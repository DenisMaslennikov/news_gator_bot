from typing import Sequence

from app.bot.handlers.keyboards.repo import get_news_sources_repo
from app.db.models import NewsSource
from app.db.session import session_scope


async def get_news_sources() -> Sequence[NewsSource]:
    """
    Получение списка источников новостей.
    :return: Список источников новостей.
    """
    async with session_scope() as session:
        return await get_news_sources_repo(session)
