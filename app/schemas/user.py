from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    created: Optional[datetime] = None


class UserRegister(UserBase):
    email: EmailStr
    password: str


class UserAuth(BaseModel):
    access_token: str


class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
