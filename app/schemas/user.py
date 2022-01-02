from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    created: Optional[datetime] = None


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserPasswordChange(BaseModel):
    oldpassword: str
    newpassword: str
