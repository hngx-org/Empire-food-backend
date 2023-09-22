from typing import Optional
from app.schemas.user_schemas import UserCreate
from pydantic import BaseModel


class CreateOrganizationSchema(BaseModel):
    organization_name: str
    lunch_price: Optional[float] = 1000.00


class OrganizationSchema(BaseModel):
    id: int
    name: str
    lunch_price: Optional[float] = 1000.00

    class Config:
        from_attributes = True


class CreateOrganizationUserSchema(UserCreate):
    otp_token: str
