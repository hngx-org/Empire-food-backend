from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from app.db import database
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user( user:UserCreate, db:Session = Depends(database.get_db()),):
  userExists = get_user_by_email(user.email)
  if userExists:
     raise HTTPException(status_code=409, detail="User already exists")
  user_db.create_user(user, db=db)


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