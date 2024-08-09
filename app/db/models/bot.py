from sqlalchemy import Column, Integer
from sqlalchemy.orm import Relationship

from app.db.models.base import Base


class User(Base):
    """Информация о пользователе telegram."""
    __tablename__ = 'bot_users'

    user_id = Column(Integer, primary_key=True)

    subscriptions = Relationship('UserSubscription', back_populates='user')
