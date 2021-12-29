import os
from datetime import datetime, timedelta
from typing import Dict

from jose import jwt
from models.user import User
from passlib.context import CryptContext
from schemas.user import UserPasswordChange, UserRegister
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_password_verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, str]):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=120)
    to_encode.update({"exp": expire})

    SECRET_KEY, ALGORITHM = os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def post_user(db: Session, obj_in: UserRegister):
    email, password = obj_in.email, get_password_hash(obj_in.password)
    db_obj = User(email=email, password=password)
    db.add(db_obj)
    db.commit()
    return create_access_token({"sub": email})


def update_user_password_by_id(db: Session, user_id: int, obj_in: UserPasswordChange):
    SUCCESS_PASSWORD_CHANGE, OLDPASSWORD_NOT_MATCH = True, False

    user = db.query(User).filter(User.id == user_id).first()
    if not get_password_verify(obj_in.oldpassword, user.password):
        return OLDPASSWORD_NOT_MATCH

    user.password = get_password_hash(obj_in.newpassword)
    db.commit()
    return SUCCESS_PASSWORD_CHANGE


def delete_user_by_id(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
