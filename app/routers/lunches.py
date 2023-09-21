from typing import Annotated

from fastapi import APIRouter, Depends, status

from db.database import get_db
from models import lunch_models, user_models
from models.user_models import User
from services.user_services import get_user_by_token


router = APIRouter()


# Redeem lunch by updating 'redeemed' field
@router.put('/api/lunch/redeem/:{id}')
async def redeem_lunch(id: str, user: User = Depends(get_user_by_token), session = Depends(get_db)):

    # Get lunch obj using id
    lunch_obj = session.query(lunch_models.Lunch).get(id)

    # Check if current user owns the lunch obj
    if user.id == lunch_obj.receiver_id:
        if lunch_obj.redeemed:
            return "Lunch has already been redeemed"
        else:
            lunch_obj.redeemed = True

            return {
                "message": "Lunch redeemed successfully",
                "statusCode": status.HTTP_201_CREATED,
                "data": None
            }