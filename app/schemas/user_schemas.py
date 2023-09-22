from typing import Optional
from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    email: EmailStr


class UserLogin(UserBase):
    password: str


class UserCreate(UserLogin):
    first_name: str
    last_name: str
    phone_number: str

class UserSearchSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    profile_pic: Optional[str] = None
    email: str
    phone: str
    is_admin: bool


class UserProfileSchema(UserSearchSchema):
    
    bank_number: Optional[str] = None
    bank_code: Optional[str] = None
    bank_name: Optional[str] = None



class UserLoginSchema(BaseModel):
    id: int
    email: EmailStr
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    is_admin: bool = False


   

