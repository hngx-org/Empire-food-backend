from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.schemas.user_schemas import UserCreate


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name='JWT')

# JWT Stuff
SECRET_KEY = 'secret key here'
ALGORITHM = 'HS256' # subject to change
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_user(db:Session, user:UserCreate):

  pass


def get_user(db:Session, user_id:int):

  pass


def get_user_by_email(db:Session, email:str):

  pass


def validate_email():
  
    pass

def validate_passowrd():
  
    pass

async def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)]):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )
   
  try:
    payload = jwt.decode(token, SECRET_KEY,     algorithms=[ALGORITHM])
    user_id = payload.get("sub")
      
    if user_id is None:
      raise credentials_exception
      
  except JWTError:
    raise credentials_exception
  
  user = get_user(user_id=user_id)
  if user is None:
    raise credentials_exception
  
  return user