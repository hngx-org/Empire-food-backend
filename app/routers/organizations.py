import datetime
from app.services.user_services import hash_password, compare_password, get_user
from app.middleware.jwt_handler import create_access_token
from app.services.helper import generate_otp, send_otp_to_email, OTPVerificationMixin
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.organization_models import  OrganizationInvite, Organization
from app.schemas.organization_schemas import CreateOrganizationSchema, OrganizationSchema, CreateOrganizationUserSchema
from app.db.database import get_db
from app.models import user_models, User


router = APIRouter(tags=["Organizations"], prefix="/organization")

@router.post('/staff/signup', status_code=status.HTTP_201_CREATED)
async def register_user_in_organization(
        user: CreateOrganizationUserSchema, db: Session = Depends(get_db)
):

    usr_instance = db.query(User).filter(User.email == user.email).first()
    if usr_instance:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    org_instance = db.query(OrganizationInvite).filter(OrganizationInvite.token==user.otp_token).first()
    otp_mixin = OTPVerificationMixin()
    if not otp_mixin.verify_otp(user.otp_token, org_instance.org_id):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Incorrect OTP')
    # existing_usr = db.query(User).filter(
    #     (User.org_id == org_instance.org_id) and (User.email == user.email)
    # ).first()
    # if existing_usr:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user with {user.email} already belongs to an organization"
    #     )
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone_number,
        is_admin=False,
        org_id=org_instance.org_id
    )
    db.add(new_user)
    db.delete(org_instance)
    db.commit()
    db.refresh(new_user)
    access_tok = create_access_token(data={'user_id': new_user.id})
    return {
        'message': 'User registered successfully',
        'statusCode': 201,
        'data': {
            'access_token': access_tok,
            'email': new_user.email,
            'id': new_user.id,
            'isAdmin': new_user.is_admin
        }
    }

@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=OrganizationSchema
)
async def create_organization(
        org: CreateOrganizationSchema, db: Session = Depends(get_db),
        role: user_models.User = Depends(get_user)
):
    """
    Create an organization.

    This endpoint allows an admin user to create an organization

    Args:
        org: The organization details
        db: The database session
        role: The admin user making the request

    Returns:
        The created organization
    """
    if role.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already is an admin to an organization"
        )
    new_org = org.model_dump()
    org_name = new_org.pop('organization_name')
    new_org['name'] = org_name
    new_org = Organization(**new_org)
    new_org.currency_code = 'NG'
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    role.org_id = new_org.id
    role.is_admin = True
    db.commit()
    return new_org