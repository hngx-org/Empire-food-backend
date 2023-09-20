from datetime import datetime, timedelta

from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .db.database import get_db
from .models.user_models import User
from .schemas.user_schemas import UserResponseSchema

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", default=30)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return access_token


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    refresh_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return refresh_token


def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
        user_id = payload.get("id")
    except JWTError:
        raise HTTPException(
            detail="Invalid refresh token",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user.refresh_token != refresh_token:
        raise HTTPException(
            detail="Invalid refresh token",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    access_token = create_access_token({"id": user.id})

    return access_token


def verify_access_token(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to verify credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = payload.get("id")
    except JWTError:
        raise credentials_exception

    if not user_id:
        raise credentials_exception

    return user_id


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserResponseSchema:
    """Gets user's token

    Protected endpoints that require user to be authenticated will include this function as a dependency in the function definition.

    As per the FastAPI documentation: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

    """

    user_id = verify_access_token(token)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist.")

    return user
