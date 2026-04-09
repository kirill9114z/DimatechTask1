from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.models.account import Account
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


async def get_admin_me(current_user: User) -> User:
    # Админ уже есть в токене — просто возвращаем
    return current_user


async def create_user(data: UserCreate, db: AsyncSession) -> User:
    # Проверяем что email не занят
    result = await db.execute(select(User).where(User.email == data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {data.email} already exists"
        )

    new_user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        is_admin=False,  # новый юзер всегда обычный пользователь
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # обновить объект после commit (получить id)
    return new_user


async def update_user(user_id: int, data: UserUpdate, db: AsyncSession) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем только переданные поля (exclude_unset — ключевой момент)
    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession) -> None:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()


async def get_all_users_with_accounts(db: AsyncSession) -> list[User]:
    # selectinload делает 2 запроса: один за юзерами, второй за их аккаунтами
    # Это лучше чем joinedload для списков — нет дублирования строк
    result = await db.execute(
        select(User)
        .where(User.is_admin == False)  # только обычные пользователи
        .options(selectinload(User.accounts))
    )
    return result.scalars().all()