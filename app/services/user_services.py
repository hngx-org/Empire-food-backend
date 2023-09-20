
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.user_schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):

    pass


def get_user(db: Session, user_id: int):

    pass


def get_user_by_email(db: Session, email: str):

    pass


def validate_email():

    pass


def validate_passowrd():

    pass


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
