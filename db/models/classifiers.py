from sqlalchemy import SmallInteger, String, Column

from db.models.base import Base


class ParseExpressionType(Base):
    __tablename__ = 'cl_parse_expression_type'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)


class NewsCategory(Base):
    __tablename__ = 'cl_news_category'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)


class NewsSourceType(Base):
    __tablename__ = 'cl_news_source_type'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)
