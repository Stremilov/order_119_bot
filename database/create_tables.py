from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///goldenLike.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class VideoProject(Base):
    """
    Класс для создания таблицы видеоработы
    """
    __tablename__ = 'videoproject'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("team.id"))
    description = Column(String(255), nullable=False)

    team = relationship("Team", back_populates="videoproject")

    def __repr__(self):
        return f"{self.id}, {self.team_id}, {self.description}"


class Team(Base):
    """
    Класс для создания таблицы команд
    """
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    team_name = Column(String, nullable=False)

    user = relationship('User', back_populates='team')
    videoproject = relationship("VideoProject", back_populates="team")

    def __repr__(self):
        return f"{self.id}, {self.team_name}, {self.user_id}"


class User(Base):
    """
    Класс для создания таблицы пользователей
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(40), nullable=False)
    team_id = Column(Integer, ForeignKey("team.id"))

    team = relationship("Team", backref="user")

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.team_name}"



