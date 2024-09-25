from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Literal
from database import models


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        user = self.db.query(models.User).where(models.User.username == username).first()
        if user:
            return user
        return None

    # !!! Не уверен в вариантах Literal
    def create_user(self, username: str, role: Literal['user', 'admin'], telegram_id: int):
        new_user = models.User(username=username, role=role, telegram_id=telegram_id)
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except IntegrityError:
            return None
        return new_user


