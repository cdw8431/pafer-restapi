from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserUpdate


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def post_user(db: Session, obj_in: UserCreate):
    db_obj = User(email=obj_in.email, password=obj_in.password)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_user_by_id(db: Session, user_id: int, obj_in: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    user.password = obj_in.password
    db.commit()


def delete_user_by_id(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
