from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate
from app.models import organization_models, user_models
from app.Responses.response import WithdrawalResponse
from app.schemas.withdrawal_schema import Withdraw

router = APIRouter(prefix="/withdrawal", tags=["Withdrawal"])


# response_model=to fit the required response
@router.post("/request", status_code=201, response_model=WithdrawalResponse)
def withdraw_request(
    withdraw: Withdraw,
    user: user_models.User = Depends(authenticate),
    db: Session = Depends(get_db),
):
    org = (
        db.query(organization_models.Organization)
        .filter(organization_models.Organization.id == user.org_id)
        .first()
    )
    org_lunch_price = org.lunch_price
    if withdraw.amount > user.lunch_credit_balance:
        # return appropriate error response with either 403 or 404
        raise HTTPException(
            status_code=404, detail="Balance is less than withdraw amount"
        )
    amount_left = user.lunch_credit_balance - withdraw.amount
    created_at = datetime.now()
    withdraw_amount = withdraw.amount * org_lunch_price
    new_withdrawal = user_models.Withdrawal(
        user_id=user.id,
        status="success",
        amount=withdraw_amount,
        created_at=created_at,
    )
    user_query = db.query(user_models.User).filter(
        user_models.User.id == user.id
    )
    user_query.update(
        {"lunch_credit_balance": amount_left}, synchronize_session=False
    )
    db.add(new_withdrawal)
    db.commit()
    db.refresh(new_withdrawal)
    # return according to specified schema
    return WithdrawalResponse(
        message="Withdrawal request created successfully",
        statusCode=201,
        data=jsonable_encoder(new_withdrawal),
    )


# handle errors
