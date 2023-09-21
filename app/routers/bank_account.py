from fastapi import APIRouter,Depends,HTTPException
from app.schemas.bankdetails_schema import BankDetailsCreate,BankDetailsResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.middleware.authenticate import authenticate
from app.models.user_models import User
from app.services.user_services import get_current_user


# This Endpoint was written by Neon

router=APIRouter(prefix="/user/bank")

# Get user bank details done for Okoh Emmanuel
@router.get("")
def get_account_details(db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
    auth_user=db.query(User).filter(User.id==user_id).first()
    if not auth_user:
            raise HTTPException(
            403,detail={"Unauthenticated":"User not found"}
        )
    return {"bank_name":auth_user.bank_name,"bank_number":auth_user.bank_number}

@router.post("")
def create_bank_details(data:BankDetailsCreate,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
    # query the user model to retrieve the authenticated user
    auth_user=db.query(User).filter(User.id==user_id)
    if not auth_user.first():
        raise HTTPException(
            404,detail={"Unauthenticated":"User not found"}
        )
    else:
        auth_user.first().bank_name=data.bank_name
        auth_user.first().bank_code=data.bank_code
        auth_user.first().bank_number=data.bank_number
        db.commit()
        return {"message":"Successfully created bank account","StatusCode":200}

