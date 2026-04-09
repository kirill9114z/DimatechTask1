from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed: list[str]
    SECRET_KEY: str
    PAYMENT_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int

def get_settings() -> Settings:
    return Settings(
        DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname",
        cors_allowed = ['http://localhost:3000'],
        SECRET_KEY="your_secret_key",
        PAYMENT_KEY="gfdmhghif38yrf9ew0jkf32",
        ACCESS_TOKEN_EXPIRE_MINUTE=30,
    )

settings = get_settings()

