from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import hashlib

pwd_context = CryptContext(
    schemes=["argon2"],   # 👈 ONLY argon2
    deprecated="auto",
)

ALGORITHM = settings.ALGORITHM


def hash_password(password: str) -> str:
    pre_hash = hashlib.sha256(password.encode("utf-8")).digest()
    return pwd_context.hash(pre_hash)

def verify_password(password: str, hashed: str) -> bool:
    pre_hash = hashlib.sha256(password.encode("utf-8")).digest()
    return pwd_context.verify(pre_hash, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
