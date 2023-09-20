from fastapi import APIRouter
<<<<<<< HEAD

router = APIRouter(tags=["Users"], prefix="/user")
=======
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user

app = APIRouter()


@app.post("apii/auth/user/signup")

async def signup(request: UserCreate):
    pass
>>>>>>> 5b87443aa3865367dd5ff0d3800966dd4b0d6c47
