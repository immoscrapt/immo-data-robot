from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.hash import argon2

from app.core.config import settings
from app.models.user import User


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return argon2.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return argon2.hash(password)

    @staticmethod
    def create_token(subject: Any, expires_delta: timedelta | None = None, token_type: str = "access") -> str:
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
        payload = {
            "sub": str(subject),
            "exp": expire,
            "type": token_type,
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError as exc:
            raise ValueError("Invalid token") from exc

    @staticmethod
    def create_access_token(subject: Any) -> str:
        return AuthService.create_token(subject, timedelta(minutes=settings.access_token_expire_minutes), "access")

    @staticmethod
    def create_refresh_token(subject: Any) -> str:
        return AuthService.create_token(subject, timedelta(minutes=settings.refresh_token_expire_minutes), "refresh")
