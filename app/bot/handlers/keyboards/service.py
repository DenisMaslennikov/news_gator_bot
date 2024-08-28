from typing import Sequence

from app.db.models import Category, Resource
from app.db.repo import get_categories_for_resources_repo, get_news_resources_repo
from app.db.session import async_session_scope


async def get_news_sources() -> Sequence[Resource]:
    """
    Получение списка источников новостей.

    :return: Список новостных ресурсов.
    """
    async with async_session_scope() as session:
        return await get_news_resources_repo(session)


async def get_categories_for_resources(resource_id: str) -> Sequence[Category]:
    """
    Получение списка категорий для ресурса.

    :param resource_id: Идентификатор ресурса.
    :return: Список доступных для подписки категорий для выбранного ресурса.
    """
    async with async_session_scope() as session:
        return await get_categories_for_resources_repo(session, resource_id)
