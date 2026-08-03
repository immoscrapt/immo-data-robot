from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.user import UserCRUD
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: Session = Depends(get_async_session)):
    existing_user = UserCRUD.get_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = UserCRUD.create(session, user_in)
    return user


@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_async_session)):
    result = session.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_async_session)):
    user = UserCRUD.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, session: Session = Depends(get_async_session)):
    user = UserCRUD.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserCRUD.update(session, user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_async_session)):
    user = UserCRUD.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    UserCRUD.delete(session, user)
