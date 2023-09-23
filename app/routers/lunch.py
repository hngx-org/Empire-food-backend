# sendlunch router created by @dyagee

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate
from app.models.lunch_models import Lunch
from app.models.user_models import User
from app.Responses.response import (
    GetAllLunchesResponse,
    GetLunchResponse,
    SendLunchResponse,
)
from app.schemas.lunch_schemas import SendLunch
from app.services.lunch_services import (
    fetch_lunch,
    get_user_lunches,
    sendLunch,
)

app = APIRouter(tags=["Lunch"])


@app.post("/lunch/send", response_model=SendLunchResponse)
async def send_lunch(
    data: SendLunch,
    current_user: User = Depends(authenticate),
    db: Session = Depends(get_db),
):
    """
    Send lunch to an authenticated user.
    """
    # extract sender id and send the lunch

    user_id = current_user.id

    # check for the total max amount, then send
    response = sendLunch(db=db, data=data, user_id=user_id)
    if response:
        return {
            "message": "Lunch request created successfully",
            "statusCode": 201,
            "data": jsonable_encoder(response),
        }

    raise HTTPException(
        status_code=404,
        detail="An error Occured; max of 4 lunch can be sent once",
    )


@app.get("/lunch/all", status_code=200, response_model=GetAllLunchesResponse)
async def get_all_lunches(
    user: User = Depends(authenticate), db: Session = Depends(get_db)
):
    """
    Gets all Lunches that have not been redeemed by the user.
    Params: user_id
    """

    user_id = user.id

    lunches = get_user_lunches(db=db, user_id=user_id)

    return {
        "message": "Lunches retrieved successfully",
        "statusCode": 200,
        "data": lunches,
    }


@app.get("/lunch/{lunch_id}", response_model=GetLunchResponse)
async def get_lunch(
    lunch_id: int,
    user: User = Depends(authenticate),
    db: Session = Depends(get_db),
):
    try:
        lunch = fetch_lunch(db, lunch_id)
        response = jsonable_encoder(lunch)
    except Exception:
        raise HTTPException(status_code=404, detail="Error: Lunch not found")
    else:
        return response


# Redeem lunch by updating 'redeemed' field
@app.put("/lunch/redeem")
async def redeem_lunch(
    lunch_ids: List[str] = Query(),
    user: User = Depends(authenticate),
    session=Depends(get_db),
):
    """
    Redeem lunch by updating 'redeemed' field
    """

    for lunch_id in lunch_ids:
        # Get lunch obj using id
        lunch_obj = session.query(Lunch).get(lunch_id)

        # Check if current user owns the lunch obj
        if user.id == lunch_obj.sender_id:
            return GetLunchResponse(
                message="You cannot redeem your own lunch",
                statusCode=status.HTTP_403_FORBIDDEN,
                data=None,
            )

        elif user.id == lunch_obj.receiver_id:
            if lunch_obj.redeemed:
                return GetLunchResponse(
                    message="Lunch has already been redeemed",
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    data=None,
                )
            lunch_obj.redeemed = True

            return GetLunchResponse(
                message="Lunch redeemed successfully",
                statusCode=status.HTTP_201_CREATED,
                data=None,
            )

        else:
            return GetLunchResponse(
                message="You cannot redeem this lunch",
                statusCode=status.HTTP_405_METHOD_NOT_ALLOWED,
                data=None,
            )
