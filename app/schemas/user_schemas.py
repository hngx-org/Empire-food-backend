from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str


class UserResponseSchema(BaseModel):
    id: str
    email: str
    name: str
    access_token: str
    is_admin: bool


class UserProfileSchema(BaseModel):
    name: str
    email: str
    profile_picture: str
    phone_number: str
    bank_number: str
    bank_code: str
    bank_name: str
    is_admin: bool


class UserLoginResponse(BaseModel):
    id: int
    email: EmailStr
    access_token: str
    refresh_token: str
    is_admin: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenRequest(BaseModel):
    refresh_token: str


class UserSearchSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    profile_pic: str
    email: str
    phone: str
    is_admin: bool
