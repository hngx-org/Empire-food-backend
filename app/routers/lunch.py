from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate
from app.models.user_models import User
from app.schemas.lunch_schemas import GetLunchResponse
from app.services.lunch_services import fetch_lunch

app = APIRouter()

@app.get("lunch/{lunch_id}", response_model=GetLunchResponse)
async def get_lunch(lunch_id: int, user_id: int = Depends(authenticate), db: Session = Depends(get_db)):
    # auth_user = get_user(db, user_id)
    auth_user=db.query(User).filter(User.id==user_id).first()
    if not auth_user:
        raise HTTPException(status_code=401, detail="Error: User not found")
    else:
        lunch = fetch_lunch(db, lunch_id)

    if not lunch:
        raise HTTPException(status_code=404, detail="Error: Lunch not found")
    else:
        response = {
                    "message": "Lunch request created successfully",
                    "status_code": 201,
                    "data": {
                             "receiver_id": lunch.receiver_id,
                             "sender_id": lunch.sender_id,
                             "quantity": lunch.quantity,
                             "redeemed": lunch.redeemed,
                             "note": lunch.note,
                             "created_at": lunch.created_at,
                             "id": lunch.id
                            }
                   }

    return response
