from typing import Sequence

from app.db.repo import get_news_resources_repo
from app.db.models import NewsResource
from app.db.session import session_scope


async def get_news_sources() -> Sequence[NewsResource]:
    """
    Получение списка источников новостей.
    :return: Список источников новостей.
    """
    async with session_scope() as session:
        return await get_news_resources_repo(session)
