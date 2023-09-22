from pydantic import BaseModel
from app.schemas.user_schemas import UserProfileSchema, UserLoginSchema, UserSearchSchema
from app.schemas.lunch_schemas import LunchResponseSchema

class ResponseClass(BaseModel):
    message: str
    statusCode: int
    data: dict |None


class UserResponse(ResponseClass):
    data: UserProfileSchema


class UserLoginResponse(ResponseClass):
    data: UserLoginSchema

class UserSearchResponse(ResponseClass):
    data: list[UserSearchSchema]

class GetLunchResponse(ResponseClass):
    data: LunchResponseSchema
