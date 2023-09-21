
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(db:Session, user:UserCreate):

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

  

def get_user(db:Session, user_id:int):

  """
    Get a user by their ID from the database.
    """
  user = db.query(User).filter(User.id == user_id).first()
  return user



def get_user_by_email(db:Session, email:str):

  """
    Get a user by their email from the database.
    """
    # Retrieve the user by email
  user = db.query(User).filter(User.email == email).first()
  return user



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