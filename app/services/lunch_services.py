from sqlalchemy.orm import Session
from app.models.lunch_models import Lunch


def get_user_lunches(db: Session, user_id: int):
    
    lunches = db.query(Lunch).filter(Lunch.receiver_id == user_id, Lunch.redeemed == False).all()

    return lunches

def fetch_lunch(db: Session, lunch_id: int):
    # Perform check for null lunch_id value
    if not lunch_id:
        return False
    
    # Query lunches table in database for lunch with input ID
    lunch = db.query(Lunch).filter(Lunch.id == lunch_id).first()
    return lunch
