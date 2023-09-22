#sendlunch router created by @dyagee

from fastapi import APIRouter, Depends,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.Responses.response import GetLunchResponse
from app.services.lunch_services import fetch_lunch
from app.db.database import get_db
from  app.schemas.lunch_schemas import SendLunchResponse,SendLunch
from app.services.lunch_services import sendLunch
from app.middleware.authenticate import authenticate
from app.models.user_models import User
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.lunch_models import Lunch

from app.middleware.authenticate import authenticate

from app.models.user_models import User
from fastapi.encoders import jsonable_encoder
from app.middleware.authenticate import authenticate
from app.Responses.response import GetLunchResponse, GetAllLunchesResponse
from app.services.lunch_services import fetch_lunch, get_user_lunches

app = APIRouter(tags=["Lunch"])

@app.post("/lunch/send", response_model=SendLunchResponse)
async def send_lunch( data:SendLunch,current_user:User=Depends(authenticate), db:Session=Depends(get_db)):
    # query the user model to retrieve the authenticated user
    user_dict = current_user.model_dump(exclude_unset=True)
    user_id = user_dict["id"]
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

@app.get("lunch/{lunch_id}", response_model=GetLunchResponse)
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
    



@app.get("/lunch/{lunch_id}", response_model=GetLunchResponse)
async def get_lunch(lunch_id: int, user: User = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        lunch = fetch_lunch(db, lunch_id)
        response = jsonable_encoder(lunch)
    except Exception:
        raise HTTPException(status_code=404, detail="Error: Lunch not found")
    else:
        return response



# Redeem lunch by updating 'redeemed' field
@app.put('/lunch/redeem/')
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
        
        