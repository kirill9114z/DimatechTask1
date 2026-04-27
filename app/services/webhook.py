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
    amount_str = str(int(payload.amount)) if payload.amount == int(payload.amount) else str(payload.amount)

    data = f"{payload.account_id}{amount_str}{payload.transaction_id}{payload.user_id}"
    expected = hashlib.sha256(
        (data + settings.PAYMENT_KEY).encode("utf-8")
    ).hexdigest()

    return hmac.compare_digest(expected, payload.signature)


async def process_webhook(payload: WebhookPayload, db: AsyncSession) -> dict:

    if not _verify_signature(payload):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )

    existing_payment = await db.scalar(
        select(Payment).where(Payment.transaction_id == payload.transaction_id)
    )
    if existing_payment:
        return {"status": "already_processed", "transaction_id": payload.transaction_id}

    account = await db.scalar(
        select(Account).where(
            Account.id == payload.account_id,
            Account.user_id == payload.user_id  
        )
    )

    if not account:
        account = Account(
            id=payload.account_id,
            user_id=payload.user_id,
            balance=0.0
        )
        db.add(account)
        await db.flush()  

    payment = Payment(
        transaction_id=payload.transaction_id,
        account_id=account.id,
        user_id=account.user_id,  
        amount=payload.amount
    )
    db.add(payment)

    account.balance += payload.amount

    await db.commit()

    return {
        "status": "success",
        "transaction_id": payload.transaction_id,
        "account_id": account.id,
        "new_balance": account.balance
    }
