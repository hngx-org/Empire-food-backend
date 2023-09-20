
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(db:Session, user:UserCreate):
  
  pass
  




def get_user(db:Session, user_id:int):

  pass


def get_user_by_email(db:Session, email:str):

  pass

def search_user_by_name_or_email(db: Session, name_or_email: str):
    # Query the database to find users whose first_name, last_name, or email contains the query
    users = db.query(User).filter(
        (User.first_name.ilike(f'%{name_or_email}%')) |
        (User.last_name.ilike(f'%{name_or_email}%')) |
        (User.email.ilike(f'%{name_or_email}%'))
    ).all()

    return users

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
