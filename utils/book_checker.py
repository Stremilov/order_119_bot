from datetime import datetime
from database import session
from database.models import BookTime


def delete_past_bookings():
    today = datetime.now().date()
    today_date_int = today.month * 30 + today.day

    past_bookings = session.query(BookTime).all()

    for booking in past_bookings:
        booking_date_int = (
            int(booking.date.split(".")[0]) + int(booking.date.split(".")[1]) * 30
        )
        if booking_date_int < today_date_int:
            session.delete(booking)

    session.commit()
