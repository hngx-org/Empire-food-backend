from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db, create_database
from  app.schemas.lunch_schemas import SendLunchResponse,SendLunch
from app.services.lunch_services import sendLunch

app = APIRouter()

create_database()


@app.post("/api/lunch/send/{user_id}", response_model=SendLunchResponse)
async def send_lunch(user_id:int, data:SendLunch, db:Session=Depends(get_db)):
    return sendLunch(db,user_id,data)