from fastapi import APIRouter, Depends , HTTPException, Request
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user
from app.models.user_models import User

app = APIRouter()


@app.post("/auth/user/signup")
async def signup(request: UserCreate):
    user, error = create_user(request)
    if error:
        return {"message": error.msg, "statusCode": error.code}
    
    return {"message": "user created successfully", "statusCode": 201, "data": user}
    