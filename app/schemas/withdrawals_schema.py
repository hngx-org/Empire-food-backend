from pydantic import BaseModel



class WithdrawalRequest(BaseModel):
    bank_name: str
    bank_number: str
    bank_code: str
    amount: float

class WithdrawalResponse(BaseModel):
    message: str
    statusCode: int
    data: dict