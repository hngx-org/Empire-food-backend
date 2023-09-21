from typing import Optional

from app.schemas.user_schemas import CreateUserSchema
from pydantic import BaseModel



class CreateOrganizationUserSchema(CreateUserSchema):
    otp_token: str
