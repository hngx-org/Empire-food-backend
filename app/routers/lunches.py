from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from db.database import get_db
from models import lunch_models, user_models
from models.user_models import User
from services.user_services import get_current_user


router = APIRouter()


# Redeem lunch by updating 'redeemed' field
@router.put('/api/lunch/redeem/:{lunch_id}')
async def redeem_lunch(lunch_ids: List[str], user: User = Depends(get_current_user), session = Depends(get_db)):
    # get_current_user depends on authenticate 

    for lunch_id in lunch_ids:
    # Get lunch obj using id
        # lunch_obj = session.query(lunch_models.Lunch).filter(lunch_models.Lunch.receiver_id == user.id).first()
        lunch_obj = session.query(lunch_models.Lunch).get(lunch_id)

        # Check if current user owns the lunch obj
        if user.id == lunch_obj.sender_id:
            return "You cannot redeem your own lunch"
        
        elif user.id == lunch_obj.receiver_id:
            if lunch_obj.redeemed:
                return "Lunch has already been redeemed"
            else:
                lunch_obj.redeemed = True

                return {
                    "message": "Lunch redeemed successfully",
                    "statusCode": status.HTTP_201_CREATED,
                    "data": None
                }
            
        else:
            return "You cannot redeem this lunch"
        
        