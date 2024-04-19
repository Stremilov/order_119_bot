from database.create_tables import session, User, Team, VideoProject
from sqlalchemy import text


def add_user_to_tables(username: str, team_name: str, description: str):
    """
    Добавление пользователя в таблицы
    """
