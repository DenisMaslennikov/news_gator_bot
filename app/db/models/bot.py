from sqlalchemy import Column, Integer, Uuid, text, ForeignKey, SmallInteger
from sqlalchemy.orm import Relationship

from app.db.models.base import Base


class UserRole(Base):
    """Роли пользователя."""
    __tablename__ = 'bot_user_roles'
    id = Column(
        Uuid(as_uuid=True), primary_key=True, comment='Идентификатор', server_default=text('gen_random_uuid()'),
    )
    user_id = Column(
        Integer, ForeignKey('bot_users.user_id'), nullable=False, comment='Идентификатор пользователя телеграм',
    )
    role_id = Column(SmallInteger, ForeignKey('cl_roles.id'), comment='Идентификатор роли', nullable=False)


class User(Base):
    """Информация о пользователе telegram."""
    __tablename__ = 'bot_users'

    user_id = Column(Integer, primary_key=True, comment='Идентификатор пользователя в телеграм')

    user_subscriptions = Relationship('UserSubscription', back_populates='user')
    roles = Relationship('Role', back_populates='users', secondary=UserRole.__table__)
