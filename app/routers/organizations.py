from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.models.organization_models import Organization
from app.schemas.organization_schemas import CreateOrganizationSchema, OrganizationSchema
from app.db.database import get_db
from app.models import user_models
from app.services.user_services import get_admin_user

router = APIRouter(tags=["Organizations"], prefix="/organization")


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=OrganizationSchema
)
async def create_organization(
        org: CreateOrganizationSchema, db: Session = Depends(get_db),
        role: user_models.User = Depends(get_admin_user)
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
    new_org = org.model_dump()
    org_name = new_org.pop('organization_name')
    new_org['name'] = org_name
    new_org = Organization(**new_org)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org
