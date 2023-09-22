#sendlunch schemas created by @dyagee


from pydantic import BaseModel

class SendLunch(BaseModel):
  receiver_id: int
  quantity: int
  note: str

  class Config:
    json_schema_extra = {
      "example": {
        "receiver_id": 23,
        "quantity": 4,
        "note": "Special instructions for the lunch"
      }
    }
  


class SendLunchResponseSchema(BaseModel):
  message: str
  statusCode: int
  data: dict

class LunchResponseSchema(BaseModel):
    receiver_id: int
    sender_id: int
    quantity: int
    redeemed: bool
    note: str
    created_at: str
    id: int
