import datetime
<<<<<<< HEAD
from app.services.user_services import hash_password, compare_password, ge
from app.middleware.jwt_handler import create_access_token
from app.services.helper import generate_otp, send_otp_to_email, OTPVerificationMixin
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.organization_models import  OrganizationInvite, Organization
from app.schemas.organization_schemas import CreateOrganizationSchema, OrganizationSchema, CreateOrganizationUserSchema
=======
import secrets
import string
from app.middleware.authenticate import authenticate
from app.services.user_services import hash_password, compare_password
from app.middleware.jwt_handler import create_access_token
from app.services.helper import generate_otp, send_otp_to_email, OTPVerificationMixin
from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.organization_models import  OrganizationInvite
from app.schemas.organization_schemas import CreateOrganizationSchema, OrganizationSchema, CreateOrganizationUserSchema, OrganizationInviteRequestSchema

>>>>>>> d04647ce78be91651b31240b6c90717cc1769bf6
from app.db.database import get_db
from app.models import user_models, User


def generate_token(length=32):
    # Define the character set for the token (you can customize this)
    characters = string.ascii_letters + string.digits  # Letters and digits

    # Generate a random token using the defined character set
    token = ''.join(secrets.choice(characters) for _ in range(length))

    return token


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

<<<<<<< HEAD
@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=OrganizationSchema
)
=======


@router.post("/invite", status_code=status.HTTP_200_OK)
def create_organization_invite(
    invite_data: OrganizationInviteRequestSchema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Check if the user is an admin
    is_admin = user.is_admin 

    if not is_admin:
        raise HTTPException(status_code=401, detail="Only admin users can create organization invites")

    # Calculate the expiration time (TTL) for the invite
    expiration_time = datetime.utcnow() + datetime.timedelta(days=7)
    
    # Generate a new secure token
    invite_token = generate_token()

    # Create a new OrganizationInvite record in the database
    new_invite = OrganizationInvite(email=invite_data.email, token=invite_token, ttl=expiration_time, org_id=user.org_id)
    db.add(new_invite)
    db.commit()
    
    ## send email functionality ##

    return Response(status_code=status.HTTP_200_OK)

  
@router.post('/create', status_code=status.HTTP_201_CREATED)
>>>>>>> d04647ce78be91651b31240b6c90717cc1769bf6
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
<<<<<<< HEAD
    return new_org
=======
    db.refresh(current_user)
    return {
        'message': 'Organization created successfully',
        'statusCode': 201,
        'data': {
            'name': new_org.name,
            'id': new_org.id
        }
    }
  
  
  
@router.put('/lunch/update/{org_id}', status_code=status.HTTP_201_CREATED)
async def update_organization_launch_date(org_id: int,
        org: OrganizationLunchSchema, db: Session = Depends(get_db), current_user: User = Depends(authenticate)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have permission to perform this action')
    
    org_instance = db.query(Organization).filter(Organization.id == org_id).first()

    if not org_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You do not belong to this organization')

    if current_user.org_id != org_instance.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have permission to perform this action')
    
    org_instance.lunch_price = org.lunch_price
    org_instance.currency_code = org.currency_code
    db.commit()
    db.refresh(org_instance)

    return {
        'message': 'Organization launch date updated successfully',
        'statusCode': 201,
        'data': {
            'name': org_instance.name,
            'id': org_instance.id,
            "lunch_price": org_instance.lunch_price,
        }
    }
>>>>>>> d04647ce78be91651b31240b6c90717cc1769bf6
