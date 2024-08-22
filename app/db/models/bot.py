from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, Uuid, text
from sqlalchemy.orm import relationship

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

    user_subscriptions = relationship('UserSubscription', back_populates='user')
    roles = relationship('Role', back_populates='users', secondary=UserRole.__table__)
    news_send = relationship('NewsSend', back_populates='user')


class NewsSent(Base):
    """Информация об отправленных новостях."""
    __tablename__ = 'bot_news_sent'

    id = Column(
        Uuid(as_uuid=True), primary_key=True, comment='Идентификатор', server_default=text('gen_random_uuid()'),
    )
    user_id = Column(Integer, ForeignKey('bot_users.user_id'), nullable=False)
    news_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news.id'), nullable=False)

    user = relationship('User', back_populates='news_sent')
    news = relationship('News', back_populates='news_sent')
