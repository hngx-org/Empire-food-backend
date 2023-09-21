from fastapi import HTTPException, Request
from .jwt_handler import verify_access_token
        
def send_email(message : str , subject : str , to_email : str):
    pass

def authenticate(token: Request):
    token = token.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = token.split(" ")[1] 
    
    
    data = verify_access_token(token)
    return data['user']