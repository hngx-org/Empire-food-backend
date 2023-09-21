from fastapi import APIRouter, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.database import get_db, create_database
from  app.schemas.lunch_schemas import SendLunchResponse,SendLunch
from app.services.lunch_services import sendLunch

app = APIRouter()

create_database()


@app.post("/api/lunch/send", response_model=SendLunchResponse)
async def send_lunch(user_id:int, data:SendLunch, db:Session=Depends(get_db)):
    resp = sendLunch(db=db,data=data,user_id=user_id)
    if resp:
        return {
        "message": "Lunch request created successfully",
        "statusCode": 201,
        "data": jsonable_encoder(resp,exclude={"id","is_deleted","redeemed"})
      }
    raise HTTPException(status_code=404,detail="An error Occured; check qty of lunch sent")