from sqlalchemy import Column, Integer

from db.models.base import Base


class User(Base):
    """Информация о пользователе telegram."""
    __tablename__ = 'bot_users'

    user_id = Column(Integer, primary_key=True)
