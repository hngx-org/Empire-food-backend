from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schemas import UserCreate, UserResponseSchema
from app.services.user_services import create_user, search_user_by_name_or_email

app = APIRouter()


@app.post("/auth/user/signup")
async def signup(request: UserCreate):
    user, error = create_user(request)
    if error:
        return {"message": error.msg, "statusCode": error.code}

    return {"message": "user created successfully", "statusCode": 201, "data": user}


@app.get("/user/search/{name_or_email}")
async def search(name_or_email: str, db: Session = Depends(get_db)):
    try:
        users = search_user_by_name_or_email(db, name_or_email)
        return {"message": "User search successful", "statusCode": 200, "data": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
