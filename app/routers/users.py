from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate, get_admin_user
from app.models.user_models import User
from app.Responses.response import UserResponse, UserSearchResponse
from app.services.helper import (
    OTPVerificationMixin,
    generate_otp,
    send_forget_password_email,
)
from app.services.user_services import (
    get_org_users,
    hash_password,
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
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(err)}"
        )


@app.get("/user/all", response_model=UserSearchResponse)
def all_org_users(
    db: Session = Depends(get_db), current_user: User = Depends(authenticate)
):
    """Returns all users linked to the organization of the current user"""
    users = get_org_users(db, current_user.org_id, current_user.id)

    return UserSearchResponse(
        message="List all users successful",
        statusCode=200,
        data=jsonable_encoder(users),
    )


@app.post("/user/forget-password", status_code=status.HTTP_200_OK)
async def forget_password(email: str, db: Session = Depends(get_db)):
    """Sends a password reset link to the user's email"""
    usr_instance = db.query(User).filter(User.email == email).first()
    if not usr_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    otp = generate_otp(1024, email)
    response = send_forget_password_email(email, otp)

    if 200 <= int(response.status_code) < 300:
        return {
            "message": "Password reset otp sent successfully",
            "statusCode": 200,
            "data": {"email": email},
        }
    raise HTTPException(
        status_code=status.HTTP_408_REQUEST_TIMEOUT,
        detail="There was an error sending the email",
    )


@app.post("/user/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    email: str, otp: str, password: str, db: Session = Depends(get_db)
):
    """Resets the user's password"""
    usr_instance = db.query(User).filter(User.email == email).first()
    if not usr_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    otp_mixin = OTPVerificationMixin()
    if not otp_mixin.verify_otp(otp, 1024, email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect OTP"
        )

    usr_instance.password_hash = hash_password(password)
    db.commit()
    return {
        "message": "Password reset successful",
        "statusCode": 200,
        "data": None,
    }


@app.delete("/admin/user/{user_id}", response_model=UserResponse)
async def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    """Removes a user from the organization"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(user)
    db.commit()
    return UserResponse(
        message="User removed successfully", statusCode=200, data=None
    )
