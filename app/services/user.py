from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User
from app.db.models.account import Account
from app.db.models.payment import Payment


async def get_me(current_user: User) -> User:
    """
    Просто возвращаем текущего юзера из токена.
    Никакого запроса в БД не нужно — объект уже есть.
    """
    return current_user


async def get_my_accounts(current_user: User, db: AsyncSession) -> list[Account]:
    """
    Возвращаем список счетов текущего пользователя.
    selectinload загружает связанные объекты одним дополнительным запросом,
    что необходимо в async SQLAlchemy — lazy load там не работает.
    """
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )
    return result.scalars().all()


async def get_my_payments(current_user: User, db: AsyncSession) -> list[Payment]:
    """
    Возвращаем список платежей текущего пользователя.
    Джойним через account чтобы убедиться что платежи именно этого юзера.
    """
    result = await db.execute(
        select(Payment).where(Payment.user_id == current_user.id)
    )
    return result.scalars().all()