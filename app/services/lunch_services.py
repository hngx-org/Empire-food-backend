from app.models.lunch_models import Lunch
from app.db.database import get_db
from sqlalchemy.orm import Session

def get_user_lunches(db: Session, user_id: int):
     return db.query(Lunch).filter(Lunch.receiver_id == user_id).all()
