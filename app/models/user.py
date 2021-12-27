from sqlalchemy import Column, Date, Integer, String

from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True)
    password = Column(String(256), nullable=False)
    created = Column(Date, default=datetime.now)
