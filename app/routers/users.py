from fastapi import APIRouter, Depends , HTTPException, Request
from app.schemas.user_schemas import UserCreate,UserProfileSchema,StaffSignupRequest
from app.services.user_services import create_user,get_current_user
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import random


app = APIRouter()



@app.post("/auth/user/signup")
async def signup(request: UserCreate):
    user, error = create_user(request)
    if error:
        return {"message": error.msg, "statusCode": error.code}
    
    return {"message": "user created successfully", "statusCode": 201, "data": user}


@app.get("/user/profile")
async def user_profile(current_user: UserProfileSchema = Depends(get_current_user)):
    return {"message": "User data fetched successfully",
            "statusCode": 200,
            "data": current_user
    }
    


#random number for now idealy should be coming from better function
def generate_otp():
    # Generate a random 6-digit OTP
    otp = ''.join(random.choice('0123456789') for _ in range(6))
    return otp


@app.post("/api/organization/staff/signup", tags=["Staff"])
async def staff_signup(request: StaffSignupRequest):
    # Check if the email already exists in the database
    
    db = SessionLocal()
    user = db.query(StaffSignupRequest).filter(StaffSignupRequest.email == request.email).first()
    if user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user record
    new_user = StaffSignupRequest(**request.dict())
    db.add(new_user)
    db.commit()
    db.close()

    otp = generate_otp(request.email)

    # Store user data in the database 
    StaffSignupRequest[request.email] = request

    return {"message": "Signup successful", "otp": otp}
