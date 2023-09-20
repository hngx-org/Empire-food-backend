from pydantic import BaseModel
from typing import Optional, Any


class TokData(BaseModel):
    id: Optional[Any] = None
