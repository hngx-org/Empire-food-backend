from pydantic import BaseModel

class RedeemRequest(BaseModel):
    ids: list[int]

