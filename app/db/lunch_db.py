from app.models.lunch_models import Lunch
from sqlalchemy.orm import Session


def view_lunch(db: Session, lunch_id: int) -> Lunch: 
    """
    """
    # Query lunches table in database for lunch with input ID
    lunch = db.query(Lunch).filter(Lunch.id == lunch_id).first()
    return lunch
