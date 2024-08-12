from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text, Uuid, text
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
    url = Column(Text, nullable=False, comment='Адрес новостного ресурса')
    update_interval = Column(Integer, nullable=False, comment='Частота обновления в секундах')
    title = Column(String(255), nullable=False, comment='Название новостного ресурса')
    comment = Column(Text, comment='Комментарий')
    parser_id = Column(Integer, ForeignKey('cl_parsers.id'), nullable=False, comment='Идентификатор парсера')
    source_type_id = Column(
        SmallInteger,
        ForeignKey('cl_resource_type.id', ondelete='RESTRICT'),
        nullable=False,
        comment='Идентификатор типа новостного ресурса',
    )

    parser = relationship('Parser', back_populates='news_resources')
    resource_type = relationship('ResourceType')
    remote_categories = relationship('RemoteCategory', back_populates='resource')


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
    update_interval = Column(Integer, nullable=True, comment='Интервал обновление в секундах')
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


class News(Base):
    """Новости."""
    __tablename__ = 'nf_news'

    id = Column(
        Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'), comment='Идентификатор новости',
    )
    title = Column(Text, nullable=False, comment='Заголовок новости')
    description = Column(Text, nullable=False, comment='Краткий анонс новости')
    content = Column(Text, comment='Текст новости')
    news_url = Column(Text, unique=True, nullable=False, comment='Ссылка на новость')
    published_at = Column(DateTime, nullable=False, comment='Дата публикации')
    detected_at = Column(DateTime, nullable=False, comment='Дата добавления в базу')
    author = Column(Text, comment='Информация об авторе')

    remote_categories = relationship(
        'RemoteCategory', back_populates='news', secondary=NewsRemoteCategory.__table__,
    )


class NewsImage(Base):
    """Изображения к новостям."""
    __tablename__ = 'nf_news_images'

    id = Column(Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    file_name = Column(String, nullable=False)
    news_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news.id', ondelete='CASCADE'), nullable=False)

    news = relationship('News')


class UserSubscription(Base):
    """Подписки пользователя."""
    __tablename__ = 'nf_user_subscription'

    id = Column(Uuid(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(Integer, ForeignKey('bot_users.user_id', ondelete='CASCADE'), nullable=False)
    resource_id = Column(
        Uuid(as_uuid=True), ForeignKey('nf_resources.id', ondelete='CASCADE'), nullable=False,
    )
    category_id = Column(
        SmallInteger, ForeignKey('cl_categories.id', ondelete='CASCADE'), nullable=False,
    )

    user = relationship('User', back_populates='subscriptions')
    resource = relationship('Resource')
    category = relationship('Category')
