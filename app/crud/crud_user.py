from typing import List, Optional

from core.security import create_access_token, get_password_hash, get_password_verify
from models.user import User
from schemas.user import UserAuth, UserPasswordChange
from sqlalchemy.orm import Session


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def post_user(db: Session, obj_in: UserAuth) -> str:
    email, password = obj_in.email, get_password_hash(obj_in.password)
    db_obj = User(email=email, password=password)
    db.add(db_obj)
    db.commit()
    return create_access_token({"sub": email})


def update_user_password_by_id(
    db: Session, user_id: int, obj_in: UserPasswordChange
) -> int:
    OLDPASSWORD_NOT_MATCH: int = 0
    SUCCESS_PASSWORD_CHANGE: int = 1
    USER_NOT_EXISTS: int = 2

    user: Optional[User] = db.query(User).filter(User.id == user_id).first()
    if not user:
        return USER_NOT_EXISTS
    elif not get_password_verify(obj_in.oldpassword, user.password):
        return OLDPASSWORD_NOT_MATCH

    user.password = get_password_hash(obj_in.newpassword)
    db.commit()
    return SUCCESS_PASSWORD_CHANGE


def delete_user_by_id(db: Session, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
