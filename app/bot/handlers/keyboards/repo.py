from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import NewsSource


async def get_news_sources_repo(session: AsyncSession) -> Sequence[NewsSource]:
    """
    Получение списка источников новостей доступных для подписки из базы данных.
    :param session: Объект сессии SQLAlchemy
    :return: Список объектов NewsSource
    """
    stmt = select(NewsSource).order_by(NewsSource.title)
    result = await session.execute(stmt)
    return result.scalars().all()
