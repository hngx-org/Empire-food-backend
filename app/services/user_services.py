
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(db:Session, user:UserCreate):

  if not is_valid_email(user.email):
     return None, Response(msg="Invalid email address", code=400)
  
  if user_db.get_user(db, user.email) != None:
      return None, Response(msg="Email already exists", code=400)
  
  user.password = hash_password(user.password)

  return user_db.create_user(db, user)
  




def get_user(db:Session, user_id:int):

  pass


def get_user_by_email(db:Session, email:str):

  pass


def is_valid_email(email):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False

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