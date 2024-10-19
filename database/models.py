from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int]
    username: Mapped[str]
    role: Mapped[str] = mapped_column(String, default="user")


class BookTime(Base):
    __tablename__ = "bookTime"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str]
    startTime: Mapped[str]
    endTime: Mapped[str]
    reason: Mapped[str]
    renter: Mapped[str]
