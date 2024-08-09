from sqlalchemy import Column, SmallInteger, String

from app.db.models.base import Base


class ParseExpressionType(Base):
    """Классификатор типа выражения для парсинга."""
    __tablename__ = 'cl_parse_expression_type'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)


class NewsCategory(Base):
    """Категории для новостей."""
    __tablename__ = 'cl_news_category'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)


class NewsSourceType(Base):
    """Тип источника новости."""
    __tablename__ = 'cl_news_source_type'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)
