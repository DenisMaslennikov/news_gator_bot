from typing import Sequence

from app.db.models import Resource, Category
from app.db.repo import get_news_resources_repo, get_categories_for_resources_repo
from app.db.session import session_scope


async def get_news_sources() -> Sequence[Resource]:
    """
    Получение списка источников новостей.

    :return: Список новостных ресурсов.
    """
    async with session_scope() as session:
        return await get_news_resources_repo(session)


async def get_categories_for_resources(resource_id: str) -> Sequence[Category]:
    """

    :param resource_id: Идентификатор ресурса.
    :return: Список доступных для подписки категорий для выбранного ресурса.
    """
    async with session_scope() as session:
        return await get_categories_for_resources_repo(session, resource_id)

