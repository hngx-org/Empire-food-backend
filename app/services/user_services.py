from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user_models import User
from app.schemas.user_schemas import UserCreate, UserSearchSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    if user.password == "":
        return None, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty",
        )
    # if  user.phone_number  == "":
    #     return None, HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail='Phone number cannot be empty'
    #     )
    if user.first_name == "" or user.last_name == "":
        return None, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First name and last name cannot be empty",
        )
    password, err = validate_password(user.password)

    if err:
        return None, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=err
        )

    if db.query(User).filter(User.email == user.email).first():
        return None, HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    try:
        new_user = User(
            email=user.email,
            password_hash=hash_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone_number,
            is_admin=False,
            lunch_credit_balance=0,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user, None
    except Exception as e:
        print(e)
        return None, HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )


def validate_password(password: str):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, None


def get_org_users(
    db: Session, org_id: int, current_user: User
) -> list[UserSearchSchema]:
    """Fetches users linked to an organization"""
    try:
        if current_user.org_id is None:
            return []

        return (
            db.query(User)
            .filter(User.org_id == org_id, User.id != current_user.id)
            .all()
        )
    except Exception as err:
        print(err)


def search_user_by_name_or_email(db: Session, name_or_email: str):
    # Query the database to find users whose first_name, last_name, or email contains the query
    users = (
        db.query(User)
        .filter(
            (User.first_name.ilike(f"%{name_or_email}%"))
            | (User.last_name.ilike(f"%{name_or_email}%"))
            | (User.email.ilike(f"%{name_or_email}%"))
        )
        .all()
    )

    return [
        UserSearchSchema(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            profile_pic=user.profile_pic,
            email=user.email,
            phone=user.phone,
            is_admin=user.is_admin,
        )
        for user in users
    ]


def hash_password(password):
    """
    hash_password returns an encrypted version of the password
    """
    return pwd_context.hash(password)


def compare_password(password, hashed_password):
    """
    compare_password compares a password with a hashed password.
    It returns True if they match, False otherwise.
    """
    return pwd_context.verify(password, hashed_password)
