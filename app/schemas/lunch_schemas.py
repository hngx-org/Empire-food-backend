from pydantic import BaseModel


class LunchData(BaseModel):
    receiver_id: id,
	sender_id: id,
    quantity: int,
	redeemed: bool,
	note: str,
	created_at: str,
	id: str


class GetLunchResponse(BaseModel):
    message: str,
    status_code: int,
    data: LunchData

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Lunch request created successfully",
                "statusCode": 201,
                "data": {
                    "receiverId": 11,
                    "senderId": 7,
                    "quantity": 2,
                    "redeemed": False,
                    "note": "Special instructions for the lunch",
                    "created_at": "2023-09-21T15:56:41.716282",
                    "id": 55
	            }
            }
        }
