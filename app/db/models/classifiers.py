from sqlalchemy import Column, SmallInteger, String, DateTime, Integer
from sqlalchemy.orm import relationship

from app.db.models import UserRole
from app.db.models.base import Base


class Role(Base):
    """Классификатор ролей пользователя."""
    __tablename__ = 'cl_roles'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор роли')
    name = Column(String(50), nullable=False,comment='Роль')

    users = relationship('User', back_populates='roles', secondary=UserRole.__table__)

class Category(Base):
    """Категории для новостей."""
    __tablename__ = 'cl_categories'

    id = Column(Integer, primary_key=True, comment='Идентификатор категории новостей')
    name = Column(String(50), nullable=False, comment='Наименование новостной категории')
    deletion_datetime = Column(DateTime, nullable=True, comment='Дата удаления')

    remote_categories = relationship('RemoteCategory', back_populates='category')
    user_subscriptions = relationship('UserSubscription', back_populates='category')


class ResourceType(Base):
    """Тип источника новости."""
    __tablename__ = 'cl_resource_type'

    id = Column(SmallInteger, primary_key=True, comment='Идентификатор типа источника новостей')
    name = Column(String(50), nullable=False, comment='Наименование типа источника новостей')

    resources = relationship('Resource', back_populates='resource_type')


class Parser(Base):
    """Модель содержащая класс и имя парсера."""
    __tablename__ = 'cl_parsers'

    id = Column(Integer, primary_key=True, comment='Идентификатор парсера')
    name = Column(String(120), comment='Название парсера')
    parser_class = Column(String(120), comment='Класс парсера')

    resources = relationship('Resource', back_populates='parser')
