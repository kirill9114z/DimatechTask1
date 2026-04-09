# app/core/security.py
import hashlib
import hmac
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings

# --- Пароли ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# --- JWT ---
ALGORITHM = "HS256"

def create_access_token(user_id: int, is_admin: bool) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE
    )
    payload = {
        "sub": str(user_id),
        "is_admin": is_admin,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    # InvalidTokenError покрывает: истёкший токен, неверную подпись, кривой формат
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])


# --- Подпись webhook ---
def verify_webhook_signature(
    transaction_id: str,
    account_id: int,
    user_id: int,
    amount: float,
    signature: str,
) -> bool:
    amount_str = str(int(amount)) if amount == int(amount) else str(amount)
    data = f"{account_id}{amount_str}{transaction_id}{user_id}"
    expected = hashlib.sha256(
        (data + settings.PAYMENT_SECRET_KEY).encode("utf-8")
    ).hexdigest()
    return hmac.compare_digest(expected, signature)