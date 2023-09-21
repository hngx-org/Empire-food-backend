#sendlunch router created by @dyagee

from fastapi import APIRouter, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.database import get_db
from  app.schemas.lunch_schemas import SendLunchResponse,SendLunch
from app.services.lunch_services import sendLunch
from app.middleware.authenticate import authenticate
from app.models.user_models import User

app = APIRouter()

@app.post("/lunch/send", response_model=SendLunchResponse)
async def send_lunch( data:SendLunch,user_id:int=Depends(authenticate), db:Session=Depends(get_db)):
    # query the user model to retrieve the authenticated user
    auth_user=db.query(User).filter(User.id==user_id).first()
    if not auth_user:
        raise HTTPException(status_code=404,detail="An error Occured; user not found")
    else:
      #check for the total max amount, then send
      resp = sendLunch(db=db,data=data,user_id=user_id)
      if resp:
          return {
            "message": "Lunch request created successfully",
            "statusCode": 201,
            "data": jsonable_encoder(resp,exclude={"id","is_deleted","redeemed"})
          }
      else:
          raise HTTPException(status_code=404,detail="An error Occured; max of 4 lunch can be sent once")