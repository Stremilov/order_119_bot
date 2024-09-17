from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    role = Column(String, default="user")


class BookTime(Base):
    __tablename__ = "bookTime"

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    startTime = Column(String, nullable=False)
    endTime = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    renter = Column(String, nullable=False)
