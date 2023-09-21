from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from app.schemas.user_schemas import UserCreate,User
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from app.db.database import get_db
from passlib.context import CryptContext
from app.middleware.jwt_handler import verify_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user( user:UserCreate, db:Session = Depends(get_db()),):
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


def get_current_user(token: str, db: Session = Depends(get_db)):
     """
    Retrieves a user based on an access token.

    :param token: The access token for authentication.
    :param db: Database session.

    :return: User object if found, None if the user does not exist or the token is invalid.
    """
    try:
        data = verify_access_token(token)
        user_id = data.id
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist.")
        return user

  
  
