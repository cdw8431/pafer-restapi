import os
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_password_verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, str]) -> str:
    to_encode: Dict[str, Any] = data.copy()
    expire = datetime.now() + timedelta(minutes=120)

    SECRET_KEY, ALGORITHM = os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    return jwt.encode(
        to_encode.update({"exp": expire}) or to_encode, SECRET_KEY, ALGORITHM
    )
