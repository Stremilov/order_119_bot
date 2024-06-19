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
    username = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")

class BookTime(Base):
    __tablename__ = 'bookTime'

    id = Column(Integer, primary_key=True)
    startBook = Column(Time, nullable=False)
    endBook = Column(Time, nullable=False)
    renter = Column(String, nullable=False)


