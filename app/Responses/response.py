from typing import Optional
from pydantic import BaseModel
from app.schemas.user_schemas import UserProfileSchema, UserLoginSchema, UserSearchSchema
from app.schemas.lunch_schemas import LunchResponseSchema,SendLunchResponseSchema, RedeemLunchResponseSchema
from app.schemas.withdrawal_schema import WithdrawResponse
from typing import Optional


class Response:
    messaage: str
    statusCode: int
    data: dict


class ResponseClass(BaseModel):
    message: str
    statusCode: int
    data: Optional[dict] = None


class UserResponse(ResponseClass):
    data: UserProfileSchema


class UserLoginResponse(ResponseClass):
    data: UserLoginSchema

class UserSearchResponse(ResponseClass):
    data: list[UserSearchSchema]

class GetLunchResponse(ResponseClass):
    data: LunchResponseSchema

class GetAllLunchesResponse(ResponseClass):
    data: list[LunchResponseSchema]

class RedeemLunchResponse(ResponseClass):
    data: RedeemLunchResponseSchema

class SendLunchResponse(ResponseClass):
    data: SendLunchResponseSchema
    
class WithdrawalResponse(ResponseClass):
    data: WithdrawResponse
