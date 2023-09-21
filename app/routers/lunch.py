from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import lunch_services
from app.models.user_models import User

app = APIRouter(tags=["Lunch"])

@app.get("/lunch/all", status_code=200)
async def get_all_lunches(
    user_id : int,
    db : Session = Depends(get_db)
):
    """
        Gets all Lunches that have not been redeemed by the user.
        Params: user_id
    """
    is_valid_user = db.query(User).filter(User.id == user_id).first()

    if not is_valid_user:
        raise HTTPException(status_code=404, detail=f"User with id '{user_id}' not found")
    

    lunches = lunch_services.get_user_lunches(db=db, user_id=user_id)

    response = {
        "message" : "Lunches retrieved successfully",
        "statusCode" : 200,
        "data" : lunches
    }

    return response
    

