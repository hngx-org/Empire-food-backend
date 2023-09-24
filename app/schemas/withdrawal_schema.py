from pydantic import BaseModel


class Withdraw(BaseModel):
    bank_number: str | None = ""
    bank_code: str | None = ""
    bank_name: str | None = ""
    amount: int


class WithdrawResponse(BaseModel):
    id: int
    user_id: int
    status: str
    amount: float
    created_at: str


class WithdrawResponseSchema(BaseModel):
    id: int
    user_id: int
    status: str
    amount: int
    created_at: str
