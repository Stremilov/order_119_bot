from database import session
from database.models import BookTime


def fetch_event_for_date(date: str):
    records = session.query(BookTime).filter_by(date=date).all()
    if records:
        data = []
        for record in records:
            data.append(
                (record.startTime, record.endTime, record.reason, record.renter)
            )
        return data
    else:
        return ""
