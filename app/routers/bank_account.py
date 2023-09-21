from fastapi import APIRouter,Depends,HTTPException
from schemas.bankdetails_schema import BankDetailsCreate,BankDetailsResponse
from db.database import get_db
from sqlalchemy.orm import Session
from middleware.authenticate import authenticate
from models.user_models import User


# This Endpoint was written by Neon

router=APIRouter(prefix="api/user/bank")
@router.post("")
def create_bank_details(data:BankDetailsCreate,db:Session=Depends(get_db),user_id:int=Depends(authenticate)):
    # query the user model to retrieve the authenticated user
    auth_user=db.query(User).filter(User.id==user_id)
    if not auth_user.first():
        raise HTTPException(
            403,detail={"Unauthenticated":"User not found"}
        )
    else:
        auth_user.update(data.dict(),synchronize_session=False)
        return {"message":"Successfully created bank account","StatusCode":200}

