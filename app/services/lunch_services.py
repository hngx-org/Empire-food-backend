from sqlalchemy.orm import Session
from app.schemas.lunch_schemas import SendLunch
from app.db.lunch_db import insert_lunch
from app.db.database import get_db, create_database
#from app.models.lunch_models import Lunch

def sendLunch(db:Session, user_id:int, data:SendLunch):
  return insert_lunch(db,user_id,data)

  



