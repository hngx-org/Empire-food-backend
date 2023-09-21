from pydantic import BaseModel
from typing import Optional



class BankDetailsCreate(BaseModel):
    bank_number:str
    bank_code:str
    bank_name:str
    bank_region:Optional[str]


class BankDetailsResponse(BaseModel):
    pass
