import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.middleware.authenticate import authenticate, get_admin_user
from app.middleware.jwt_handler import create_access_token
from app.models import User, user_models
from app.models.organization_models import (
    Organization,
    OrganizationInvite,
    OrganizationLaunchWallet,
)
from app.schemas.organization_schemas import (
    CreateOrganizationSchema,
    CreateOrganizationUserSchema,
    OrganizationLunchSchema,
)
from app.services.helper import (
    OTPVerificationMixin,
    send_otp_to_email,
)
from app.services.user_services import hash_password

router = APIRouter(tags=["Organizations"], prefix="/organization")


@router.post("/staff/signup", status_code=status.HTTP_201_CREATED)
async def register_user_in_organization(
    user: CreateOrganizationUserSchema, db: Session = Depends(get_db)
):
    usr_instance = db.query(User).filter(User.email == user.email).first()
    if usr_instance:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    org_instance = (
        db.query(OrganizationInvite)
        .filter(OrganizationInvite.token == user.otp_token)
        .first()
    )
    if not org_instance:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect OTP"
        )
    otp_mixin = OTPVerificationMixin()
    if not otp_mixin.verify_otp(
        user.otp_token, org_instance.org_id, user.email
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect OTP"
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone_number,
        is_admin=False,
        org_id=org_instance.org_id,
        lunch_credit_balance=0,
    )
    db.add(new_user)
    db.delete(org_instance)
    db.commit()
    db.refresh(new_user)
    access_tok = create_access_token(new_user.id)
    return {
        "message": "User registered successfully",
        "statusCode": 201,
        "data": {
            "access_token": access_tok,
            "email": new_user.email,
            "id": new_user.id,
            "isAdmin": new_user.is_admin,
        },
    }


@router.post("/invite", status_code=status.HTTP_200_OK)
async def user_organization_invite(
    email: EmailStr,
    db: Session = Depends(get_db),
    role: user_models.User = Depends(get_admin_user),
):
    org = db.query(Organization).filter(Organization.id == role.org_id).first()

    response, code = send_otp_to_email(
        role.email, email, role.org_id, org.name
    )

    if 200 <= int(response.status_code) < 300:
        org_instance = OrganizationInvite(
            email=email,
            token=code,
            org_id=role.org_id,
            ttl=datetime.datetime.now(),
        )
        db.add(org_instance)
        db.commit()
        db.refresh(org_instance)
        return {
            "message": "success",
            "statusCode": 200,
            "data": None,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="There was an error sending the email",
        )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_organization(
    org: CreateOrganizationSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(authenticate),
):
    if org.organization_name == "":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Organization name cannot be empty",
        )

    if current_user.org_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already belongs to an organization",
        )

    org_instance = db.query(Organization)

    org_name_check = org_instance.filter(
        Organization.name == org.organization_name
    ).first()

    if org_name_check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization name already exists",
        )

    user_org_check = org_instance.filter(
        Organization.id == current_user.org_id
    ).first()

    if user_org_check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already belongs to an organization",
        )

    new_org = Organization(
        name=org.organization_name,
        lunch_price=org.lunch_price,
        currency_code=org.currency_code,
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    current_user.org_id = new_org.id
    current_user.is_admin = True

    org_wallet = OrganizationLaunchWallet(org_id=new_org.id, balance=100000)

    db.add(org_wallet)
    db.commit()
    db.refresh(current_user)
    db.refresh(org_wallet)
    return {
        "message": "Organization created successfully",
        "statusCode": 201,
        "data": {
            "name": new_org.name,
            "id": new_org.id,
            "admin": {
                "email": current_user.email,
                "id": current_user.id,
                "is_admin": current_user.is_admin,
            },
            "wallet_balance": org_wallet.balance,
        },
    }


@router.put("/lunch/update/{org_id}", status_code=status.HTTP_201_CREATED)
async def update_organization_launch_date(
    org_id: int,
    org: OrganizationLunchSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(authenticate),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )

    org_instance = (
        db.query(Organization).filter(Organization.id == org_id).first()
    )

    if not org_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You do not belong to this organization",
        )

    if current_user.org_id != org_instance.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )

    org_instance.lunch_price = org.lunch_price
    org_instance.currency_code = org.currency_code
    db.commit()
    db.refresh(org_instance)

    return {
        "message": "Organization launch date updated successfully",
        "statusCode": 201,
        "data": {
            "name": org_instance.name,
            "id": org_instance.id,
            "lunch_price": org_instance.lunch_price,
        },
    }


@router.get("/wallet", status_code=status.HTTP_200_OK)
async def get_wallet(
    db: Session = Depends(get_db), role: User = Depends(get_admin_user)
):
    """

    Get Organization Wallet

    This endpoint allows an admin user to get the organization wallet

    Args:
        db: The database session
        role: The admin user making the request

    Returns:
        The organization wallet
    """
    org_instance = (
        db.query(OrganizationLaunchWallet)
        .filter(OrganizationLaunchWallet.org_id == role.org_id)
        .first()
    )

    if not org_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return {
        "message": "success",
        "statusCode": 200,
        "data": {"balance": org_instance.balance},
    }


@router.post("/wallet", status_code=status.HTTP_200_OK)
async def update_wallet(
    amount: Decimal,
    db: Session = Depends(get_db),
    role: User = Depends(get_admin_user),
):
    """

    Update Organization Wallet

    This endpoint allows an admin user to update the organization wallet

    Args:
        balance: The organization wallet balance
        db: The database session
        role: The admin user making the request

    Returns:
        The updated organization
    """
    org_wallet = (
        db.query(OrganizationLaunchWallet)
        .filter(OrganizationLaunchWallet.org_id == role.org_id)
        .first()
    )

    if not org_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Amount cannot be negative",
        )

    org_wallet.balance += amount

    db.add(org_wallet)
    db.commit()
    db.refresh(org_wallet)

    return {
        "message": "success",
        "statusCode": 200,
        "data": {"balance": org_wallet.balance},
    }
