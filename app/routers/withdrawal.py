from datetime import datetime
from app.middleware.authenticate import authenticate, get_admin_user
from app.schemas.withdrawal_schema import Withdraw, WithdrawResponseSchema, WithdrawResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from app.db.database import get_db
from app.models import organization_models, user_models
from app.Responses.response import WithdrawalResponse, AdminWithdrawalResponse

router = APIRouter(
    prefix="/withdrawal",
    tags=['Withdrawal']
)

# response_model=to fit the required response
@router.post("/request", status_code=201, response_model=WithdrawalResponse)
def withdraw_request(withdraw: Withdraw,
                     user:user_models.User=Depends(authenticate), db: Session = Depends(get_db)):
    org = db.query(organization_models.Organization).filter(
        organization_models.Organization.id == user.org_id).first()
    org_lunch_price = org.lunch_price
    if withdraw.amount > user.lunch_credit_balance:
        # return appropriate error response with either 403 or 404
        raise HTTPException(
            status_code=404, detail='Balance is less than withdraw amount')
    amount_left = user.lunch_credit_balance - withdraw.amount
    created_at = datetime.now()
    withdraw_amount = withdraw.amount * org_lunch_price
    new_withdrawal = user_models.Withdrawal(user_id=user.id, status="success", amount=withdraw_amount,
                                            created_at=created_at)
    user_query = db.query(user_models.User).filter(
        user_models.User.id == user.id)
    user_query.update({"lunch_credit_balance": amount_left},
                      synchronize_session=False)
    db.add(new_withdrawal)
    db.commit()
    db.refresh(new_withdrawal)
    # return according to specified schema
    return WithdrawalResponse(message="Withdrawal request created successfully", statusCode=201, data=jsonable_encoder(new_withdrawal))
# handle errors

# @router.get('/user/all', status_code=status.HTTP_200_OK, response_model=list[WithdrawalResponse])
# async def get_all_withdrawals(user: user_models.User = Depends(authenticate), db: Session = Depends(get_db)):
#     """Returns all withdrawals linked to the organization of the current user"""
#     withdrawals = db.query(user_models.Withdrawal).filter(
#         user_models.Withdrawal.user_id == user.id).all()
#     return withdrawals

# @router.get('/admin/all', status_code=status.HTTP_200_OK, response_model=list[AdminWithdrawalResponse])
# async def get_all_withdrawals_for_admin(role: user_models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
#     """Returns all withdrawals linked to the organization of all users"""
#     ret_table = []
#     all_users = db.query(user_models.User).filter(user_models.User.org_id == role.org_id).all()
#     for user in all_users:
#         withdrawals = db.query(user_models.Withdrawal).filter(
#         user_models.Withdrawal.user_id == user.id).all()
#         ret_table.append({
#             'user_id': user.id,
#             'data': [WithdrawResponseSchema(**withdrawal.model_dump()) for withdrawal in withdrawals]
#         })
#     return ret_table


@router.get('/user/all', status_code=status.HTTP_200_OK, response_model=list[WithdrawResponse])
async def get_all_withdrawals(user: user_models.User = Depends(authenticate), db: Session = Depends(get_db)):
    """Returns all withdrawals linked to the organization of the current user"""
    withdrawals = (
        db.query(user_models.Withdrawal)
        .filter(user_models.Withdrawal.user_id == user.id)
        .all()
    )
    return withdrawals

@router.get('/admin/all', status_code=status.HTTP_200_OK, response_model=list[AdminWithdrawalResponse])
async def get_all_withdrawals_for_admin(role: user_models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    """Returns all withdrawals linked to the organization of all users"""
    query = (
        db.query(user_models.User)
        .filter(user_models.User.org_id == role.org_id)
        .subquery()
    )
    
    withdrawals = (
        db.query(
            user_models.User.id.label("user_id"),
            user_models.Withdrawal.id,
            user_models.Withdrawal.status,
            user_models.Withdrawal.amount,
            user_models.Withdrawal.created_at
        )
        .join(query, user_models.User.id == query.c.id)
        .filter(user_models.Withdrawal.is_deleted == False)  # Filter out deleted withdrawals
        .all()
    )
    
    ret_table = {}
    
    for withdrawal in withdrawals:
        user_id = withdrawal.user_id
        if user_id not in ret_table:
            ret_table[user_id] = {"user_id": user_id, "data": []}
        
        withdrawal_data = {
            "id": withdrawal.id,
            "status": withdrawal.status,
            "amount": withdrawal.amount,
            "created_at": withdrawal.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        ret_table[user_id]["data"].append(withdrawal_data)
    
    return list(ret_table.values())

