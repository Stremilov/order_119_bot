from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import models


class BookTimeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_bookings_by_date(self, date: str, fetch: bool = False):
        bookings = self.db.query(models.BookTime).filter_by(date=date).all()

        if fetch and bookings:
            data = []
            for record in bookings:
                data.append(
                    (record.startTime, record.endTime, record.reason, record.renter)
                )
            return data
        elif fetch:
            return ''
        return bookings

    # Не оч согласен с тем, как оформлена БД. Может стоит хранить в таблице не юзернеймы, а указатели в таблицу юзеров?
    def get_bookings_by_username(self, username: str):
        bookings = self.db.query(models.BookTime).filter(models.BookTime.renter == username).order_by(
            models.BookTime.id).all()
        return bookings

    def create_ticket(self, date: str, start_time: str, end_time: str, renter: str, reason: str):
        new_ticket = models.BookTime(
            date=date,
            startTime=start_time,
            endTime=end_time,
            renter=renter,
            reason=reason,
        )
        try:
            self.db.add(new_ticket)
            self.db.commit()
            self.db.refresh(new_ticket)
        except IntegrityError:
            return None
        return new_ticket

    def delete_ticket(self, date: str, start_time: str, end_time: str):
        ticket = self.db.query(models.BookTime).filter(
            models.BookTime.date == date,
            models.BookTime.startTime == start_time,
            models.BookTime.endTime == end_time,
        ).first()

        if ticket:
            self.db.delete(ticket)
            self.db.commit()
        return ticket
