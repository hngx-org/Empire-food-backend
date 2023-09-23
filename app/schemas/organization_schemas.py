from typing import Optional
from app.schemas.user_schemas import UserCreate
from pydantic import BaseModel, EmailStr


class CreateOrganizationSchema(BaseModel):
    organization_name: str
    lunch_price: Optional[float] = 1000.00
    currency_code: Optional[str] = 'NGN'

class OrganizationSchema(BaseModel):
    id: int
    name: str
    lunch_price: Optional[float] = 1000.00
    currency_code: Optional[str] = 'NGN'

    class Config:
        from_attributes = True


class CreateOrganizationUserSchema(UserCreate):
    otp_token: str


    
class OrganizationInviteRequestSchema(BaseModel):
    email: EmailStr

class OrganizationLunchSchema(BaseModel):
    lunch_price: Optional[float] = 1000.00
    currency_code: Optional[str] = 'NGN'

