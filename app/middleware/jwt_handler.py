import time
from datetime import datetime

from fastapi import APIRouter , HTTPException, Request , status
from jose import jwt , JWTError
from app.settings import settings

setting = settings.Settings()

def create_access_token(id: int) -> str:
    payload = {
        "user": id,
        "expires": time.time() + setting.access_tok_expire_minutes
    }
    token = jwt.encode(payload, setting.secret_key, setting.algorithm)
    return token

def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token, setting.secret_key,setting.algorithm)
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!") 
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )