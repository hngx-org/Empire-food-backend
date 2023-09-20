from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str


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
