from pydantic import BaseModel


class LunchResponseData(BaseModel):
    receiver_id: int
    sender_id: int
    quantity: int
    redeemed: bool
    note: str
    created_at: str
    id: int


class GetLunchResponse(BaseModel):
    message: str
    status_code: int
    data: LunchResponseData

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Lunch request created successfully",
                "status_code": 201,
                "data": {
                    "receiverId": 11,
                    "senderId": 7,
                    "quantity": 5,
                    "redeemed": False,
                    "note": "Special instructions for the lunch",
                    "created_at": '2023-09-21T15:56:41.716282',
                    "id": 22
                }
            }
        }
