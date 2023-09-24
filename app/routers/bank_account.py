from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate
from app.models.user_models import User
from app.schemas.bankdetails_schema import BankDetailsCreate

# This Endpoint was written by Neon

router = APIRouter(prefix="/user/bank", tags=["Bank Details"])


# Get user bank details done for Okoh Emmanuel
@router.get("")
def get_account_details(
    db: Session = Depends(get_db), user: User = Depends(authenticate)
):
    # auth_user=db.query(User).filter(User.id==user.id)
    if not user:
        raise HTTPException(403, detail={"Unauthenticated": "User not found"})
    return {
        "message": "Bank details",
        "StatusCode": 200,
        "data": {
            "bank_name": user.bank_name,
            "bank_number": user.bank_number,
            "bank_code": user.bank_code,
        },
    }


@router.post("")
def create_bank_details(
    data: BankDetailsCreate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate),
):
    if not user:
        raise HTTPException(404, detail={"Unauthenticated": "User not found"})

    user.bank_name = data.bank_name
    user.bank_code = data.bank_code
    user.bank_number = data.bank_number
    user.bank_region = data.bank_region
    db.commit()
    return {
        "message": "Successfully created bank account",
        "StatusCode": 200,
        "data": "null",
    }
