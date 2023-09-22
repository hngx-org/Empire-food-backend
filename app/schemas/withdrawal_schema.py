from pydantic import BaseModel

class Withdraw(BaseModel):
    bank_number: str
    bank_code: str
    bank_name: str
    amount: int