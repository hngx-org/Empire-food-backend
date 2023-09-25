# sendlunch services created by @dyagee


from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.lunch_db import insert_lunch
from app.models.lunch_models import Lunch
from app.models.organization_models import OrganizationLaunchWallet
from app.models.user_models import User
from app.schemas.lunch_schemas import SendLunch
from sqlalchemy import or_


def sendLunch(db: Session, data: SendLunch, user_id: int, org_id: int):
    # check for max amount sent
    check = data.model_dump(exclude_unset=True)
    if check["quantity"] > 4:
        return None, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sorry, you can only send a maximum of 4 lunches at a time",
        )

    receiver = db.query(User).filter(User.id == data.receiver_id).first()

    if not receiver:
        return None, HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, the user you are trying to send lunch to does not exist",
        )

    if receiver.org_id != org_id:
        return None, HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sorry, the user you are trying to send lunch to does not belong to your organization",
        )

    # deduct from the OrgaizationLaunchWallet
    org_wallet = (
        db.query(OrganizationLaunchWallet)
        .filter(OrganizationLaunchWallet.org_id == org_id)
        .first()
    )

    if org_wallet is None:
        return None, HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, your organization does not have a lunch wallet",
        )

    if org_wallet.balance < data.quantity:
        return None, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sorry, your organization does not have enough balance to send this lunch",
        )

    org_wallet.balance = org_wallet.balance - data.quantity

    db.commit()
    db.refresh(org_wallet)
    res = insert_lunch(db=db, user_id=user_id, data=data, org_id=org_id)
    if res:
        return res, None
    return None, HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Sorry, your lunch could not be sent",
    )


def get_user_lunches(db: Session, user_id: int, param: str = None):
    if param == "sent":
        lunches = db.query(Lunch).filter(Lunch.sender_id == user_id).all()
    elif param == "received":
        lunches = db.query(Lunch).filter(Lunch.receiver_id == user_id).all()
    else:
        # check both lucnhes sent and recieved
        lunches = db.query(Lunch).filter(or_(Lunch.sender_id == user_id, Lunch.receiver_id == user_id)).all()
    
    return lunches


def fetch_lunch(db: Session, lunch_id: int):
    # Perform check for null lunch_id value
    if not lunch_id:
        return False

    # Query lunches table in database for lunch with input ID
    return db.query(Lunch).filter(Lunch.id == lunch_id).first()
