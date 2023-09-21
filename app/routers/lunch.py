from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schemas import UserCreate
from app.services.user_services import lunch_services
from app.db.database import get_db
from sqlalchemy.orm import Session

app = APIRouter()

@app.get("/lunch/{lunch_id}")
async def get_lunch(lunch_id: int, db : Session = Depends(get_db)):
    lunch = lunch_services.get_lunch(lunch_id, db)

    if lunch is None:
        raise HTTPException(status_code=404, detail="Lunch not found")
    else:
           response = {
            "message": "Lunch request created successfully",
            "statusCode": 201,
            "data": {
                    "receiverId": lunch.receiverId,
                    "senderId": lunch.senderId,
                    "quantity": lunch.quantity,
                    "redeemed": lunch.redeemed,
                    "note": lunch.note,
                    "created_at": lunch.created_at,
                    "id": lunch.id
                }
            }
           
           return response
