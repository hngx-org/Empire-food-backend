from app.db.lunch_db import view_lunch
from sqlalchemy.orm import Session


def fetch_lunch(db: Session, lunch_id: int):
    # Perform check for null lunch_id value
    if not lunch_id:
        return False
    lunch = view_lunch(db, lunch_id)
    return lunch
