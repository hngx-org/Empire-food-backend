from fastapi import APIRouter,Depends
from schemas.bankdetails_schema import BankDetailsCreate,BankDetailsResponse
router=APIRouter(prefix="api/user/bank")
from db.database import get_db
from sqlalchemy.orm import Session


@router.post("")
def create_bank_details(data:BankDetailsCreate,db:Session=Depends(get_db)):
    pass
