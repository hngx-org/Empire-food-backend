import time
from datetime import datetime , timedelta

from fastapi import APIRouter , HTTPException , status , Depends

from jose import JWTError, jwt
from app.settings import settings

setting = settings.Settings()

def create_token(id: int , expiry_time:int) -> str:
    payload = {
        "user": id,
        "expires": time.time() + expiry_time
    }
    token = jwt.encode(payload, setting.secret_key, setting.algorithm)
    return token

def create_access_token(id : int):
    return create_token(id , setting.access_tok_expire_minutes)

def create_refresh_token(id : int):
    return create_token(id , setting.refresh_tok_expire_minutes)


def verify_token(token: str) -> int:
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
        return data['user']
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
        
'''
def refresh_access_token(refresh_token, db: Session = Depends(get_db)):
    id = verify_token(refresh_token)

    user = db.query(User).filter(User.id == id ).first()

    if not user:
        raise HTTPException(detail="User does not exist.", status_code=404)
    elif user.refresh_token != refresh_token:
        raise HTTPException(
            detail="Invalid refresh token",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return create_access_token(id)
    
'''
