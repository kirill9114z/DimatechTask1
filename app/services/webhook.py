import hashlib
import hmac

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.account import Account
from app.db.models.payment import Payment
from app.schemas.payment import WebhookPayload


def _verify_signature(payload: WebhookPayload) -> bool:
    """
    Формула из ТЗ: {account_id}{amount}{transaction_id}{user_id}{secret_key}
    Ключи в алфавитном порядке: account_id, amount, transaction_id, user_id

    Важно: amount форматируем без лишних нулей (100.0 → "100", 99.5 → "99.5")
    чтобы совпасть с тем что присылает сторонняя система
    """
    amount_str = str(int(payload.amount)) if payload.amount == int(payload.amount) else str(payload.amount)

    data = f"{payload.account_id}{amount_str}{payload.transaction_id}{payload.user_id}"
    expected = hashlib.sha256(
        (data + settings.PAYMENT_KEY).encode("utf-8")
    ).hexdigest()

    # compare_digest защищает от timing-атак — всегда используй его вместо ==
    return hmac.compare_digest(expected, payload.signature)


async def process_webhook(payload: WebhookPayload, db: AsyncSession) -> dict:

    # 1. Проверяем подпись
    if not _verify_signature(payload):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )

    # 2. Идемпотентность: если транзакция уже обработана — возвращаем 200 без ошибки
    existing_payment = await db.scalar(
        select(Payment).where(Payment.transaction_id == payload.transaction_id)
    )
    if existing_payment:
        return {"status": "already_processed", "transaction_id": payload.transaction_id}

    # 3. Проверяем существует ли счёт у этого пользователя
    account = await db.scalar(
        select(Account).where(
            Account.id == payload.account_id,
            Account.user_id == payload.user_id   # счёт должен принадлежать именно этому юзеру
        )
    )

    # 4. Если счёта нет — создаём
    if not account:
        account = Account(
            id=payload.account_id,
            user_id=payload.user_id,
            balance=0.0
        )
        db.add(account)
        await db.flush()  # flush чтобы account.id был доступен до commit

    # 5. Сохраняем транзакцию
    payment = Payment(
        transaction_id=payload.transaction_id,
        account_id=account.id,
        user_id=account.user_id,   # берём из аккаунта, не из payload — гарантия консистентности
        amount=payload.amount
    )
    db.add(payment)

    # 6. Начисляем сумму на счёт
    account.balance += payload.amount

    # 7. Один commit для всех изменений — атомарность
    await db.commit()

    return {
        "status": "success",
        "transaction_id": payload.transaction_id,
        "account_id": account.id,
        "new_balance": account.balance
    }