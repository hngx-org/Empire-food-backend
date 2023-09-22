import datetime
from app.services.user_services import hash_password, compare_password
from app.middleware.jwt_handler import create_access_token
from app.services.helper import generate_otp, send_otp_to_email, OTPVerificationMixin
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.organization_models import  OrganizationInvite
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


