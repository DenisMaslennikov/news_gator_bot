from sqlalchemy import Column, DateTime, ForeignKey, Integer, Interval, SmallInteger, String, Text, Uuid, text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Resource(Base):
    """Источники новостей."""
    __tablename__ = 'nf_resources'

    id = Column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
        comment='Идентификатор новостного ресурса',
    )
    url = Column(Text, nullable=False, comment='Адрес новостного ресурса', unique=True)
    update_interval = Column(Interval, nullable=False, comment='Частота обновления в секундах')
    update_datetime = Column(DateTime, nullable=True, comment='Дата и время последнего обновления')
    title = Column(String(255), nullable=False, comment='Название новостного ресурса')
    comment = Column(Text, comment='Комментарий')
    parser_id = Column(Integer, ForeignKey('cl_parsers.id'), nullable=False, comment='Идентификатор парсера')
    source_type_id = Column(
        SmallInteger,
        ForeignKey('cl_resource_type.id', ondelete='RESTRICT'),
        nullable=False,
        comment='Идентификатор типа новостного ресурса',
    )

    parser = relationship('Parser', back_populates='resources')
    resource_type = relationship('ResourceType', back_populates='resources')
    remote_categories = relationship('RemoteCategory', back_populates='resource')
    user_subscriptions = relationship('UserSubscription', back_populates='resource')


class NewsRemoteCategory(Base):
    """Таблица для связи многий ко многим новостей с категориями."""
    __tablename__ = 'nf_news_remote_categories'

    id = Column(Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'), comment='Идентификатор')
    remote_category_id = Column(Uuid(as_uuid=True), ForeignKey('nf_remote_categories.id'), nullable=False)
    news_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news.id'), nullable=False)


class RemoteCategory(Base):
    """Категории новостей на новостном ресурсе."""
    __tablename__ = 'nf_remote_categories'

    id = Column(
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text('gen_random_uuid()'),
        comment='Идентификатор категории ресурса'
    )
    name = Column(String(100), comment='Название категории', nullable=False)
    url = Column(Text, comment='Ссылка на категорию', nullable=False)
    news_resource_id = Column(Uuid(as_uuid=True), ForeignKey('nf_resources.id'), nullable=False)
    update_interval = Column(Interval, nullable=True, comment='Интервал обновление в секундах')
    update_datetime = Column(DateTime, nullable=True, comment='Дата и время последнего обновления')
    category_id = Column(
        Integer, ForeignKey('cl_categories.id'), nullable=True, comment='Локальная категория новостей',
    )
    parser_id = Column(Integer, ForeignKey('cl_parsers.id'), comment='Идентификатор парсера')
    deletion_datetime = Column(DateTime, comment='Дата и время удаления')
    notification_datetime = Column(
        DateTime, comment='Дата и время когда было выслано уведомление о добавлении категории',
    )

    news = relationship('News', back_populates='remote_categories', secondary=NewsRemoteCategory.__table__)
    category = relationship('Category', back_populates='remote_categories')
    resource = relationship('Resource', back_populates='remote_categories')
    parser = relationship('Parser', back_populates='remote_categories')


class News(Base):
    """Новости."""
    __tablename__ = 'nf_news'

    id = Column(
        Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'), comment='Идентификатор новости',
    )
    title = Column(Text, nullable=False, comment='Заголовок новости')
    description = Column(Text, nullable=True, comment='Краткий анонс новости')
    content = Column(Text, comment='Текст новости')
    news_url = Column(Text, unique=True, nullable=False, comment='Ссылка на новость')
    published_at = Column(DateTime, nullable=True, comment='Дата публикации')
    detected_at = Column(DateTime, nullable=False, comment='Дата добавления в базу')
    author = Column(Text, comment='Информация об авторе')

    remote_categories = relationship(
        'RemoteCategory', back_populates='news', secondary=NewsRemoteCategory.__table__,
    )
    images = relationship('Image', back_populates='news')
    news_send = relationship('NewsSend', back_populates='news')


class Image(Base):
    """Изображения к новостям."""
    __tablename__ = 'nf_images'

    id = Column(Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    file_name = Column(String, nullable=False)
    news_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news.id', ondelete='CASCADE'), nullable=False)

    news = relationship('News', back_populates='images')


class UserSubscription(Base):
    """Подписки пользователя."""
    __tablename__ = 'nf_user_subscription'

    id = Column(Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(Integer, ForeignKey('bot_users.user_id', ondelete='CASCADE'), nullable=False)
    resource_id = Column(
        Uuid(as_uuid=True), ForeignKey('nf_resources.id', ondelete='CASCADE'), nullable=True,
    )
    category_id = Column(
        SmallInteger, ForeignKey('cl_categories.id', ondelete='CASCADE'), nullable=True,
    )

    user = relationship('User', back_populates='user_subscriptions')
    resource = relationship('Resource', back_populates='user_subscriptions')
    category = relationship('Category', back_populates='user_subscriptions')
