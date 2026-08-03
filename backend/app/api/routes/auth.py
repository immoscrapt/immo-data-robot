from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud.user import UserCRUD
from app.db.session import get_async_session
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_async_session),
):
    user = UserCRUD.get_by_email(session, form_data.username)
    if not user or not AuthService.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return Token(
        access_token=AuthService.create_access_token(user.id),
        refresh_token=AuthService.create_refresh_token(user.id),
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, session: Session = Depends(get_async_session)):
    existing_user = UserCRUD.get_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = UserCRUD.create(session, user_in)
    return user
