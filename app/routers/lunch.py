from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_models import User
from fastapi.encoders import jsonable_encoder
from app.middleware.authenticate import authenticate
from app.Responses.response import GetLunchResponse, GetAllLunchesResponse
from app.services.lunch_services import fetch_lunch, get_user_lunches

app = APIRouter(tags=["Lunch"])

@app.get("/lunch/all", status_code=200, response_model=GetAllLunchesResponse)
async def get_all_lunches(
    user: User = Depends(authenticate),
    db : Session = Depends(get_db)
):
    """
        Gets all Lunches that have not been redeemed by the user.
        Params: user_id
    """

    user_id = user.id    

    lunches = get_user_lunches(db=db, user_id=user_id)

    response = {
        "message" : "Lunches retrieved successfully",
        "statusCode" : 200,
        "data" : lunches
    }

    return response
    



@app.get("lunch/{lunch_id}", response_model=GetLunchResponse)
async def get_lunch(lunch_id: int, user: User = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        lunch = fetch_lunch(db, lunch_id)
        response = jsonable_encoder(lunch)
    except Exception:
        raise HTTPException(status_code=404, detail="Error: Lunch not found")
    else:
        return response
