from pydantic import BaseModel


class LunchResponseSchema(BaseModel):
    receiver_id: int
    sender_id: int
    quantity: int
    redeemed: bool
    note: str
    created_at: str
    id: int
