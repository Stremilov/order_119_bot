from aiogram import executor

from database.get_users_by_team_name import get_usernames_by_team_name
from database.add_user_to_tables import add_user_to_tables
from loader import dp
from database.create_tables import engine, Base, User, session, Team, VideoProject
from sqlalchemy import text
import handlers


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # get_usernames_by_team_name(team_name='TeamB')
    executor.start_polling(dp, skip_updates=True)
