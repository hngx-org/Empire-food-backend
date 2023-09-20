from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.user_models import User


def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
