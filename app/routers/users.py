from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate
from app.models.user_models import User
from app.Responses.response import UserResponse, UserSearchResponse
from app.services.user_services import (
    get_org_users,
    search_user_by_name_or_email,
)

app = APIRouter(tags=["Users"])


@app.get("/user/profile", response_model=UserResponse)
async def user_profile(current_user: User = Depends(authenticate)):
    return {
        "message": "User data fetched successfully",
        "statusCode": 200,
        "data": jsonable_encoder(current_user),
    }


@app.get("/user/search/{name_or_email}", response_model=UserSearchResponse)
async def search(
    name_or_email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(authenticate),
):
    try:
        users = search_user_by_name_or_email(db, name_or_email)
        return UserSearchResponse(
            message="User search successful",
            statusCode=200,
            data=jsonable_encoder(users),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )


@app.get("/user/all", response_model=UserSearchResponse)
def all_org_users(
    db: Session = Depends(get_db), current_user: User = Depends(authenticate)
):
    """Returns all users linked to the organization of the current user"""
    users = get_org_users(db, current_user.org_id)
    return UserSearchResponse(
        message="User search successful",
        statusCode=200,
        data=jsonable_encoder(users),
    )
