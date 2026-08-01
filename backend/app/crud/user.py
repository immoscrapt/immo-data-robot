from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from passlib.hash import argon2

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def create(session: AsyncSession, user_in: UserCreate) -> User:
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
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update(session: AsyncSession, user: User, user_in: UserUpdate) -> User:
        if user_in.full_name is not None:
            user.full_name = user_in.full_name
        if user_in.role is not None:
            user.role = user_in.role.value
        if user_in.is_active is not None:
            user.is_active = user_in.is_active
        user.updated_at = datetime.utcnow()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.commit()
