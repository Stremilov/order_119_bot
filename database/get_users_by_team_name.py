from database.create_tables import session, User, Team


def get_usernames_by_team_name(team_name: str):
    """
    Получение участников команды по названию команды
    """
    people_in_team = session.query(User.username).join(Team).filter(Team.team_name == team_name).all()

    for person in people_in_team:
        ...
        # код для вывода информации пользователю
