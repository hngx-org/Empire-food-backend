from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.login_schema import LoginSchema, LoginResponseSchema
from ..models.user_models import Users
from ..services.user_services import verify_password


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
def login(user_credentials: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Users).filter(
        Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    if not verify_password(user_credentials.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    return {'message': 'Login successful', "token": "exampleToken"}
