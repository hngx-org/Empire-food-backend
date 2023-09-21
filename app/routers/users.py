from fastapi import APIRouter
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user

app = APIRouter()


@app.post("api/auth/user/signup")
async def signup(request: UserCreate):
    pass
