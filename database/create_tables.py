from aiogram.types import CallbackQuery
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy.orm import sessionmaker, declarative_base

from loader import dp, bot

engine = create_engine("sqlite:///orderDatabase.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    role = Column(String, default="user")

class BookTime(Base):
    __tablename__ = 'bookTime'

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    startTime = Column(String, nullable=False)
    endTime = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    renter = Column(String, nullable=False)


