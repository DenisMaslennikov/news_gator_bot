from typing import List, Tuple, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import class_mapper, joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad

from app.db.models.base import Base


async def get_or_create(session: AsyncSession, model: Type[Base], **kwargs) -> Tuple[Base, bool]:
    """
    Создать или получить объект модели.

    :param session: Сессия SQLAlchemy.
    :param model: Модель.
    :param kwargs: Именованные аргументы модели.
    :return: Кортеж объект модели и False если объект не был создан True если создан новый объект в базе.
    """
    stmt = select(model).filter_by(**kwargs)
    result = await session.execute(stmt)
    instance = result.scalars().first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True


def joinedload_all_relationships(model: Type[Base]) -> List[_AbstractLoad]:
    """
    Динамически создает список options для joinedload всех связей модели.

    :param model: Модель для которой необходимо подгрузить связанные модели.
    :return: Список связей обернутый в joinedload() для использования в options запроса.
    """
    options = []
    for name, rel in class_mapper(model).relationships.items():
        options.append(joinedload(getattr(model, name)))
    return options
