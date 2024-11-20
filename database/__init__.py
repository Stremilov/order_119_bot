from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass

# DATABASE_URL = f"postgresql+psycopg2://postgres:postgres@db:5432/order_119"

engine = create_engine("sqlite:///orderDatabase.db", pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)
session = Session()
