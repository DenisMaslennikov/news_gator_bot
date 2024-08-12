from sqlalchemy import Column, SmallInteger, String, DateTime, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Roles(Base):
    """Классификатор ролей пользователя."""
    __tablename__ = 'cl_roles'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор роли')
    name = Column(String(50), nullable=False,comment='Роль')

class Category(Base):
    """Категории для новостей."""
    __tablename__ = 'cl_categories'

    id = Column(Integer, primary_key=True, comment='Идентификатор категории новостей')
    name = Column(String(50), nullable=False, comment='Наименование новостной категории')
    deletion_datetime = Column(DateTime, nullable=True, comment='Дата удаления')

    remote_categories = relationship('RemoteCategory', back_populates='category')


class NewsSourceType(Base):
    """Тип источника новости."""
    __tablename__ = 'cl_news_source_type'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор типа источника новостей')
    name = Column(String(50), nullable=False, comment='Наименование типа источника новостей')


class Parser(Base):
    """Модель содержащая класс и имя парсера."""
    __tablename__ = 'cl_parsers'

    id = Column(Integer, primary_key=True, comment='Идентификатор парсера')
    name = Column(String(120), comment='Название парсера')
    parser_class = Column(String(120), comment='Класс парсера')

    news_resources = relationship('NewsResource', back_populates='parser')
