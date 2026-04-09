from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_admin
from app.db.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate, User, UserAccount
from app.services import admin as admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/me", response_model=User)
async def get_admin_me(
    current_admin: UserModel = Depends(require_admin)
):
    return await admin_service.get_admin_me(current_admin)


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await admin_service.create_user(data, db)


@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await admin_service.update_user(user_id, data, db)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    await admin_service.delete_user(user_id, db)


@router.get("/users", response_model=list[UserAccount])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await admin_service.get_all_users_with_accounts(db)