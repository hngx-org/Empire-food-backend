from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .jwt_handler import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
        
def send_email(message : str , subject : str , to_email : str):
    pass

def authenticate(token: str = Depends(oauth2_scheme)):
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = token.split(" ")[1] 
    
    
    data = verify_token(token)
    return data