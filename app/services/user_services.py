
from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from app.schemas.user_schemas import UserCreate
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from app.db.database import get_db
from passlib.context import CryptContext
from app.middleware.jwt_handler import verify_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(db:Session, user:UserCreate):
  
  pass
  




def get_user(db:Session, user_id:int):

  pass


def get_user_by_email(db:Session, email:str):

  pass


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


#expects the oauth2_scheme  
"""
    retreive user_id from verified token and queries the data base for the user info.
    returns user data if found, raise a HTTPException if not.
    """
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  data = verify_access_token(token)
  user_id = data.get("id")
  user = db.query(User).filter(User.id == user_id).first()
  if user:
    return user
  else:
   raise  HTTPException(status_code=400, detail="User does not exist.")
  
  
  