from app.models.lunch_models import Lunch
from sqlalchemy.orm import Session


def fetch_lunch(db: Session, lunch_id: int) -> Lunch:
    # Perform check for null lunch_id value
    if not lunch_id:
        return False
    
    # Query lunches table in database for lunch with input ID
    lunch = db.query(Lunch).filter(Lunch.id == lunch_id).first()
    return lunch
