from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User
from app.db.models.account import Account
from app.db.models.payment import Payment


async def get_me(current_user: User) -> User:
    return current_user


async def get_my_accounts(current_user: User, db: AsyncSession) -> list[Account]:
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )
    return result.scalars().all()


async def get_my_payments(current_user: User, db: AsyncSession) -> list[Payment]:
    result = await db.execute(
        select(Payment).where(Payment.user_id == current_user.id)
    )
    return result.scalars().all()
