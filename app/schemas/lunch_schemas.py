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
  


class SendLunchResponse(BaseModel):
  message: str
  statusCode: int
  data: dict

  class Config:
    json_schema_extra = {
      "example": {
        "message": "Lunch request created successfully",
        "statusCode": 201,
        "data": {}
      }
    }