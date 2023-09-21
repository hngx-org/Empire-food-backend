from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.lunch_models import Lunches

def get_lunch(db:Session, lunch_id:int):
    
    lunch = db.query(Lunches).filter(lunch_id == Lunches.id).first()

    return lunch