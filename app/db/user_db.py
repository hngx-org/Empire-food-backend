from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.user_models import Users
from datetime import datetime
from uuid import uuid4
from app.Responses.response import Response


def get_user(db: Session, user_id: int):
    """
    Get a user by their ID from the database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    return user


# add user to database
def create_user(db: Session, user: UserCreate):
    """
    Create a new user and add them to the database.
    """
    # Create a new User model instance
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password_hash=hash_password(user.password),
        is_admin=user.is_admin,
        lunch_credit_balance=user.lunch_credit_balance,
        refresh_token=user.refresh_token,
        bank_number=user.bank_number,
        bank_code=user.bank_code,
        bank_name=user.bank_name,
        bank_region=user.bank_region,
        currency=user.currency,
        currency_code=user.currency_code,
    )

    # Add the user to the database session and commit the transaction
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

