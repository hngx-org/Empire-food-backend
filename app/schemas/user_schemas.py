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
    profile_pic: str |None = None
    email: str
    phone: str
    is_admin: bool


class UserProfileSchema(UserSearchSchema):
    
    bank_number: str |None = None
    bank_code: str |None = None
    bank_name: str |None = None



class UserLoginSchema(BaseModel):
    id: int
    email: EmailStr
    access_token: str | None = None
    refresh_token: str | None = None
    is_admin: bool = False


   

