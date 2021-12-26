from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRes(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    created: Optional[date] = None

    class Config:
        orm_mode = True