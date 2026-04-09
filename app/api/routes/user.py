from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models.user import User
from app.schemas.user import User
from app.schemas.account import Account
from app.schemas.payment import PaymentResponse
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
async def get_user(
    current_user: User = Depends(get_current_user)
):
    return await user_service.get_me(current_user)


@router.get("/me/accounts", response_model=list[Account])
async def get_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await user_service.get_my_accounts(current_user, db)


@router.get("/me/payments", response_model=list[PaymentResponse])
async def get_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await user_service.get_my_payments(current_user, db)