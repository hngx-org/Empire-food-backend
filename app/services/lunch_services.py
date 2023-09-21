#sendlunch services created by @dyagee


from sqlalchemy.orm import Session
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

  



