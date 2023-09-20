from pydantic import BaseModel
from datetime import datetime

class LunchResponse(BaseModel):
    id : int
    org_id : int
    sender_id: str
    receiver_id : int
    quantity: int
    redeemed : bool
    note: str
    created_at : datetime