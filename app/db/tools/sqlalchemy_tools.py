from typing import Type, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import Base


async def get_or_create(session: AsyncSession, model: Type[Base], **kwargs) -> Tuple[Base, bool]:
    stmt = select(model).filter_by(**kwargs)
    result = await session.execute(stmt)
    instance = result.scalar_one_or_none()

    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        await session.flush()

        return instance, True

