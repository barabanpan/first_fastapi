from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from email_validator import validate_email, EmailNotValidError

from app.users.models import User
from app.users.schemas import UserLogin, UserSignUp, UserLoginResponse
from app.auth.services import (
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, authenticate_user,
    create_access_token, create_refresh_token, create_password_hash)


auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    description="Login with user's email & password"
)
async def login(user: UserLogin):
    """Endpoint for token authentication."""
    user = await authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "is_admin": user.is_admin, "type": "access"},
        expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email, "is_admin": user.is_admin, "type": "refresh"},
        expires_delta=refresh_token_expires
    )
    login_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "access_expired_in": ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_expired_in": REFRESH_TOKEN_EXPIRE_MINUTES,
        "is_admin": user.is_admin,
        "user_id": user.id,
    }
    return UserLoginResponse(**login_data)


@auth_router.post("/sign-up", response_model=User)
async def sign_up(user: UserSignUp):
    """Sign up a new user."""
    try:
        valid = validate_email(user.email)
        """Update with the normalized form."""
        email = valid.email
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Wrong email address provided: '{user.email}'",
            headers={"WWW-Authenticate": "Bearer"}
        )

    new_user = User(
        id=str(uuid4()),
        email=email,
        hashed_password=create_password_hash(user.password),
        is_admin=user.is_admin,
        joined=datetime.utcnow().timestamp(),
        is_active=True
    )

    try:
        await new_user.save()
    except Exception as e:  # IntegrityError
        # print("EXCEPTION:", repr(e))

        """Return error message if email is already in the database."""
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with email {email} already exists.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return new_user
