from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session
from .jwt_handler import verify_token
from app.db.database import get_db
from app.models.user_models import User

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
        
def send_email(message : str , subject : str , to_email : str):
    pass

def authenticate(access_token: str = Header(), db: Session= Depends(get_db)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_id = verify_token(access_token)
    
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="failed to authenticate user")
