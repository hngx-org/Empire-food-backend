from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
  email:str
  password: str
  first_name: str
  last_name: str
  phone_number: str


class UserResponseSchema(BaseModel):
  id:str
  email:str
  name: str
  access_token: str
  is_admin: bool