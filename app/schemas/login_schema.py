from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class LoginResponseSchema(BaseModel):
    username: str
    token: str
    role: str
    id: int

    class Config:
        orm_mode = True
