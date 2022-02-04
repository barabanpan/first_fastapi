from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import Config
from app.users.models import User


SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.HASHING_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(Config.ACCESS_TOKEN_EXPIRE_MINUTES)
# ? app_password = settings.app_password


"""Generate password hash."""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def get_user(user: str):
    """
    Search the database for user.

    For login, searching is by email.
    For function get_current_user, searching is by id.
    """
    if "@" in user:
        user_in_db = User.objects.get(email=user)
    else:
        user_in_db = User.objects.get(id=user)

    try:
        print(user_in_db)
    except IndexError as err:
        print(f"Err: {err}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Operation not permitted, wrong id or email provided: '{user}'",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user_in_db


def authenticate_user(email, password):
    """Authenticate user by checking they exist and that the password is correct."""
    user = get_user(email)
    if not user:
        return False

    """If present, verify password against password hash in database."""
    password_hash = user.hashed_password

    if not verify_password(password, password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token, required for OAuth2 flow."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(HTTPBearer())):
    """Decrypt the token and retrieve the username from payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(user=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Check that current user is not disabled and return the user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
