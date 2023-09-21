
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate

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




