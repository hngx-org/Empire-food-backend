from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.user_models import User
from datetime import datetime
from uuid import uuid4



def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()