from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.hash import argon2

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD:
    @staticmethod
    def get_by_email(session: Session, email: str) -> User | None:
        result = session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> User | None:
        result = session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    def create(session: Session, user_in: UserCreate) -> User:
        now = datetime.utcnow()
        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=argon2.hash(user_in.password),
            role=user_in.role.value,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(session: Session, user: User, user_in: UserUpdate) -> User:
        if user_in.full_name is not None:
            user.full_name = user_in.full_name
        if user_in.role is not None:
            user.role = user_in.role.value
        if user_in.is_active is not None:
            user.is_active = user_in.is_active
        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete(session: Session, user: User) -> None:
        session.delete(user)
        session.commit()
