from typing import Optional

from pydantic import BaseModel


class CreateOrganizationSchema(BaseModel):
    organization_name: str
    lunch_price: float


class OrganizationSchema(BaseModel):
    id: int
    organization_name: str
    lunch_price: Optional[float] = 1000.00

    class Config:
        orm_mode = True
