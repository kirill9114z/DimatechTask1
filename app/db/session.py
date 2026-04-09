from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.DATABASE_URL)
Sessionlocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with Sessionlocal() as session:
        try:
            yield session
        finally:
            await session.close()

