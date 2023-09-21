from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import lunch_services

app = APIRouter(tags=["Lunch"])

@app.get("/lunch", status_code=200)
async def get_all_lunches(
    user_id : int,
    db : Session = Depends(get_db)
):
    
    lunches = lunch_services.get_user_lunches(db=db, user_id=user_id)

    response = {
        "message" : "Lunches retrieved successfully",
        "statusCode" : 201,
        "data" : lunches
    }

    return response
    

