from fastapi import APIRouter, Depends, Header, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.jwt_handler import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
)
from app.models.user_models import User
from app.Responses.response import ResponseClass, UserLoginResponse
from app.schemas import user_schemas
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user

app = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/user/signup", response_model=ResponseClass, status_code=201)
async def signup(request: UserCreate, db: Session = Depends(get_db)):
    user, exception = create_user(db, request)
    if exception:
        raise exception

    return ResponseClass(
        message="User registered successfully", statusCode=201, data=None
    )


@app.post("/login", status_code=200, response_model=UserLoginResponse)
def login(credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    """Logs in user"""

    user = db.query(User).filter_by(email=credentials.email).first()

    if not user:
        raise HTTPException(
            detail="Invalid credentials.",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    # Verify user's password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            detail="Invalid credentials.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    user.refresh_token = refresh_token
    db.commit()
    db.refresh(user)
    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "email": user.email,
        "id": user.id,
        "is_admin": user.is_admin,
    }

    return UserLoginResponse(
        message="User authenticated successfully.", statusCode=201, data=data
    )


@app.post("/refresh", status_code=200)
def refresh_token(
    id: int, refresh_token: str = Header(), db: Session = Depends(get_db)
):
    """Refreshes user's access token"""

    access_token = refresh_access_token(id, refresh_token, db)

    return {
        "message": "User authenticated successfully.",
        "status_code": 200,
        "data": {"access_token": access_token},
    }


def get_authorization_token(authorization: str):
    """
    get_authorization_token returns the authorization token from the request
    expects format: Authorization: Bearer <token>
    """
    parts = authorization.split(" ")
    return None if len(parts) != 2 else parts[1]
