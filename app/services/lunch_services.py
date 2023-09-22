#sendlunch services created by @dyagee


from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.lunch_models import Lunch
from app.schemas.lunch_schemas import SendLunch
from app.db.lunch_db import insert_lunch


def sendLunch(db:Session, data:SendLunch, user_id:int):
  #check for max amount sent
  check = data.model_dump(exclude_unset=True)
  if check['quantity'] > 4:
    return False
  res = insert_lunch(db=db,user_id=user_id,data=data)
  if res:
    return res
  return False

def get_user_lunches(db: Session, user_id: int):
    
    lunches = db.query(Lunch)\
                .filter(
                    or_(
                        Lunch.receiver_id == user_id, 
                        Lunch.sender_id == user_id
                    )
                )\
                .all()

    return lunches

def fetch_lunch(db: Session, lunch_id: int):
    # Perform check for null lunch_id value
    if not lunch_id:
        return False
    
    # Query lunches table in database for lunch with input ID
    lunch = db.query(Lunch).filter(Lunch.id == lunch_id).first()
    return lunch
