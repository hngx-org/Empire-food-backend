from fastapi import APIRouter , HTTPException, Request,Depends, status
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user
from app import schemas, models
from sqlalchemy import asc
from app.db.database import engine, get_db
from sqlalchemy.orm import Session

app = APIRouter()


@app.post("/auth/user/signup")
async def signup(request: UserCreate):
    user, error = create_user(request)
    if error:
        return {"message": error.msg, "statusCode": error.code}
    
    return {"message": "user created successfully", "statusCode": 201, "data": user}


@app.get("/api/user", response_model = schemas.UserResponseSchema, status_code=status.HTTP_200_OK)
def get_persons(db:Session = Depends(get_db)):
    users = db.query(models.User).order_by(asc(models.User.id)).all()
    return {"message": "All users", "statusCode": 200, "data": users}