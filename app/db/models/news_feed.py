import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, Text, Uuid
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class NewsSource(Base):
    """Источники новостей."""
    __tablename__ = 'nf_news_source'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(Text, nullable=False)
    update_interval = Column(SmallInteger, nullable=False)
    title = Column(String(255), nullable=False)
    comment = Column(Text)
    source_type_id = Column(SmallInteger, ForeignKey('cl_news_source_type.id'), nullable=False)
    default_news_category_id = Column(SmallInteger, ForeignKey('cl_news_category.id'))

    source_type = relationship('NewsSourceType')
    default_news_category = relationship('NewsCategory')
    news = relationship('News', back_populates='source')


class ParsingExpression(Base):
    """Выражения для парсинга новостей."""
    __tablename__ = 'nf_parsing_expressions'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parse_expression_type_id = Column(SmallInteger, ForeignKey('cl_parse_expression_type.id'), nullable=False)
    parse_expression = Column(Text, nullable=False)
    news_source_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news_source.id'), nullable=False)
    parsing_level = Column(SmallInteger, nullable=False)

    parse_expression_type = relationship('ParseExpressionType')
    news_source = relationship('NewsSource')


class News(Base):
    """Новости."""
    __tablename__ = 'nf_news'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text)
    news_url = Column(Text, unique=True, nullable=False)
    news_source_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news_source.id'), nullable=False)
    news_category_id = Column(SmallInteger, ForeignKey('cl_news_category.id'), nullable=False)
    published_at = Column(DateTime, nullable=False)
    author = Column(Text)

    source = relationship('NewsSource', back_populates='news')
    category = relationship('NewsCategory')


class NewsImage(Base):
    """Изображения к новостям."""
    __tablename__ = 'nf_news_images'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    news_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news.id'), nullable=False)

    news = relationship('News')


class UserSubscription(Base):
    """Подписки пользователя."""
    __tablename__ = 'nf_user_subscription'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('bot_users.user_id'))
    news_source_id = Column(Uuid(as_uuid=True), ForeignKey('nf_news_source.id'))
    news_category_id = Column(SmallInteger, ForeignKey('cl_news_category.id'))

    user = relationship('User')
    news_source = relationship('NewsSource')
    news_category = relationship('NewsCategory')
