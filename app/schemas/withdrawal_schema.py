from pydantic import BaseModel

class Withdraw(BaseModel):
    bank_number: str
    bank_code: str
    bank_name: str
    amount: int

class WithdrawResponse(BaseModel):
    id: int
    user_id: int
    status: str
    amount: int
    created_at: str


class WithdrawResponseSchema(BaseModel):
    id: int
    user_id: int
    status: str
    amount: int
    created_at: str