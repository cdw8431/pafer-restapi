from datetime import datetime

from database import Base
from sqlalchemy import Column, Date, Integer, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True)
    nickname = Column(String(64), unique=True)
    password = Column(String(256), nullable=False)
    created_at = Column(Date, default=datetime.now)
