from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from email_validator import validate_email, EmailNotValidError

from app.users.models import User
from app.users.schemas import UserLogin, UserSignUp, UserLoginResponse #, UserResetPassword
from app.auth.services import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, create_password_hash


auth_router = APIRouter()


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    description="Login with user's email & password"
)
async def login(user: UserLogin):
    """Endpoint for token authentication."""
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    login_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "expired_in": ACCESS_TOKEN_EXPIRE_MINUTES,
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


"""@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(user_reset_pass: UserResetPassword):
    Reset User's password.

    email, new_password = user_reset_pass.email, user_reset_pass.new_password
    try:
        valid = validate_email(email)
        Update with the normalized form.
        email = valid.email
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Not valid email address was provided: '{email}'"
        )


    with neo4j_driver.session() as session:
        Checking if user exists, if not - raise 404.
        user_exists = session.run(query_check_user, email=email)
        if not user_exists.data():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        Encrypt new password.
        new_password_hash = create_password_hash(new_password)

        Update user's password with a new one.
        session.run(query_reset_password, email=email, new_password_hash=new_password_hash)

    return {"detail": "Password successfully updated"}
"""