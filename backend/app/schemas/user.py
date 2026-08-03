from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    agent = "agent"


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    full_name: str | None = None
    role: UserRole = UserRole.agent


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
