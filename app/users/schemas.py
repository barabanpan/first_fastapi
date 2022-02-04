from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserSignUp(BaseModel):
    """User sign up model."""

    email: str
    password: str
    is_admin: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "email": "example@email.com",
                "password": "SecretPass1234",
                "is_admin": False
            }
        }


class UserLogin(BaseModel):
    """User sign up model."""

    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "example@email.com",
                "password": "SecretPass1234"
            }
        }


class UserLoginResponse(BaseModel):
    """Response with tokens."""

    access_token: str
    token_type: str
    expired_in: int
    is_admin: bool
    user_id: str
