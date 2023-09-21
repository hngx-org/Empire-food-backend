from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import (
    create_access_token,
    create_refresh_token,
    refresh_access_token,
)
from app.models.user_models import User
from app.schemas import user_schemas

app = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/login", status_code=200)
def login(credentials: user_schemas.UserLogin, db: Session = Depends(get_db)):
    """Logs in user"""

    user = db.query(User).filter_by(email=credentials.email).first()

    if not user:
        raise HTTPException(
            detail="Invalid credentials.", status_code=status.HTTP_403_FORBIDDEN
        )
    else:
        # Verify user's password
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                detail="Invalid credentials.", status_code=status.HTTP_403_FORBIDDEN
            )

    access_token = create_access_token({"id": user.id})
    refresh_token = create_refresh_token({"id": user.id})

    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "email": user.email,
        "id": user.id,
        "is_admin": user.is_admin,
    }

    return {
        "message": "User authenticated successfully.",
        "status_code": 200,
        "data": user_schemas.LoginResponse(**data),
    }


@app.post("/refresh", status_code=200)
def refresh_token(token_request: user_schemas.TokenRequest):
    """Refreshes user's access token"""

    access_token = refresh_access_token(token_request.refresh_token)

    return {
        "message": "User authenticated successfully.",
        "status_code": 200,
        "data": {"access_token": access_token},
    }
