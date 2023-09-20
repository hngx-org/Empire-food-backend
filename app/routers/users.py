from fastapi import APIRouter, Depends , HTTPException, Request
from app.schemas.user_schemas import UserCreate
from app.services.user_services import create_user

app = APIRouter()



def authenticate(token: Request):
    token = token.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = token.split(" ")[1] 
    
    expected_token = None
    if token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/auth/user/signup")
async def signup(request: UserCreate, token: Depends(authenticate)):
    user, error = create_user(request)
    if error:
        return {"message": error.msg, "statusCode": error.code}
    
    return {"message": "user created successfully", "statusCode": 201, "data": user}
    