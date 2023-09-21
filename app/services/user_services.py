from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.schemas.user_schemas import UserCreate, UserSearchSchema
from app.models.user_models import User
import re
from app.settings.settings import EMAIL_REGEX
from app.Responses.response import Response
from app.db import user_db
from app.db.database import get_db
from passlib.context import CryptContext
from app.middleware.authenticate import  authenticate
from fastapi import HTTPException, status, Depends
from jose import jwt , JWTError
from app.settings.settings import Settings

from app.middleware.jwt_handler import create_access_token, create_refresh_token, refresh_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(db:Session, user:UserCreate):
  
  if db.query(User).filter(User.email == user.email).first():
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
  new_user = User(
      email=user.email,
      password_hash=hash_password(user.password),
      first_name=user.first_name,
      last_name=user.last_name,
      phone=user.phone_number,
      is_admin=False
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  access_tok = create_access_token(new_user.id)
  return {
      'message': 'User registered successfully',
      'statusCode': 201,
      'data': {
          'access_token': access_tok,
          'email': new_user.email,
          'id': new_user.id,
          'isAdmin': new_user.is_admin
      }
  }
  




def get_user(db: Session, user_id: int):
    pass


def get_user_by_email(db: Session, email: str):
    pass


def search_user_by_name_or_email(db: Session, name_or_email: str = Depends(authenticate)):
    # Query the database to find users whose first_name, last_name, or email contains the query
    users = db.query(User).filter(
        (User.first_name.ilike(f'%{name_or_email}%')) |
        (User.last_name.ilike(f'%{name_or_email}%')) |
        (User.email.ilike(f'%{name_or_email}%'))
    ).all()

    users_response = [UserSearchSchema(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        profile_pic=user.profile_pic,
        email=user.email,
        phone=user.phone,
        is_admin=user.is_admin
    ) for user in users]
    return users_response


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


def get_current_user(token: str = Depends(authenticate), db: Session = Depends(get_db)):
    """
    Retrieves a user based on an access token.

    :param token: The access token for authentication.
    :param db: Database session.

    :return: User object if found, None if the user does not exist or the token is invalid.
    """
    user_id = token.id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist.")
    return user
