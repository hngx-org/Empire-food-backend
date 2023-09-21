from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.user_models import User
from datetime import datetime
from uuid import uuid4
from app.Responses.response import Response


def get_user(db: Session, user_id: int):
    pass


# add user to database
def create_user(db: Session, user: UserCreate):
    pass

