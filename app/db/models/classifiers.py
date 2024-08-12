from sqlalchemy import Column, SmallInteger, String, DateTime

from app.db.models.base import Base


class ParseExpressionType(Base):
    """Классификатор типа выражения для парсинга."""
    __tablename__ = 'cl_parse_expression_type'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор типа выражения для парсинга')
    name = Column(String(50), nullable=False,comment='Наименование типа выражения для парсинга')


class NewsCategory(Base):
    """Категории для новостей."""
    __tablename__ = 'cl_news_category'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор категории новостей')
    name = Column(String(50), nullable=False, comment='Наименование новостной категории')
    deletion_datetime = Column(DateTime, nullable=True, comment='Дата удаления')


class NewsSourceType(Base):
    """Тип источника новости."""
    __tablename__ = 'cl_news_source_type'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор типа источника новостей')
    name = Column(String(50), nullable=False, comment='Наименование типа источника новостей')
