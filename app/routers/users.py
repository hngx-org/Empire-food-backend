from fastapi import APIRouter, Depends , HTTPException, Request
from app.schemas.user_schemas import UserCreate,UserProfileSchema
from app.services.user_services import create_user,get_current_user


app = APIRouter()



@app.post("/auth/user/signup")
async def signup(request: UserCreate):
    user, error = create_user(request)
    if error:
        return {"message": error.msg, "statusCode": error.code}
    
    return {"message": "user created successfully", "statusCode": 201, "data": user}


@app.get("/api/user/profile")
async def user_profile(current_user: UserProfileSchema = Depends(get_current_user)):
    return {"message": "User data fetched successfully",
            "statusCode": 200
            "data": current_user
    }
    

