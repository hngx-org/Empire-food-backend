from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.middleware.authenticate import authenticate

from app.models.user_models import User
from app.models.lunch_models import Lunch

from app.Responses.response import GetLunchResponse

from app.services.lunch_services import fetch_lunch

app = APIRouter()

@app.get("lunch/{lunch_id}", response_model=GetLunchResponse)
async def get_lunch(lunch_id: int, user: User = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        lunch = fetch_lunch(db, lunch_id)
        response = jsonable_encoder(lunch)
    except Exception:
        raise HTTPException(status_code=404, detail="Error: Lunch not found")
    else:
        return response



# Redeem lunch by updating 'redeemed' field
@app.put('lunch/redeem/')
async def redeem_lunch(lunch_ids: List[str] = Query(), user: User = Depends(authenticate), session = Depends(get_db)):
    """
    Redeem lunch by updating 'redeemed' field
    """

    for lunch_id in lunch_ids:
    # Get lunch obj using id
        # lunch_obj = session.query(lunch_models.Lunch).filter(lunch_models.Lunch.receiver_id == user.id).first()
        lunch_obj = session.query(Lunch).get(lunch_id)

        # Check if current user owns the lunch obj
        if user.id == lunch_obj.sender_id:
            return GetLunchResponse(
                message="You cannot redeem your own lunch",
                statusCode=status.HTTP_403_FORBIDDEN,
                data=None
            )
        
        # Update redeemed to True and save changes into DB
        elif user.id == lunch_obj.receiver_id:
            if lunch_obj.redeemed:
                return GetLunchResponse(
                    message="Lunch has already been redeemed",
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    data=None
                )
            else:
                lunch_obj.redeemed = True

                return GetLunchResponse(
                    message="Lunch redeemed successfully",
                    statusCode=status.HTTP_201_CREATED,
                    data=None
                )
            
        else:
            return GetLunchResponse(
                    message="You cannot redeem this lunch",
                    statusCode=status.HTTP_405_METHOD_NOT_ALLOWED,
                    data=None
            )
        
        