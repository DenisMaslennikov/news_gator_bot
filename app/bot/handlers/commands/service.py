from sqlalchemy.orm import subqueryload

from app.db.models import Category, Resource, User
from app.db.repo import (
    delete_all_user_subscriptions_repo,
    delete_subscription_repo,
    delete_user_repo,
    get_category_by_id_repo,
    get_news_resource_repo,
    get_subscription_repo,
    get_user_repo,
    register_user_repo,
    subscribe_user_repo,
)
from app.db.session import async_session_scope


async def register_user(user_id: int) -> bool:
    """
    Регистрация пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Строка со статусом регистрации.
    """
    async with async_session_scope() as session:
        return await register_user_repo(session, user_id)


async def delete_user(user_id: int) -> bool:
    """
    Регистрация пользователя.

    :param user_id: Идентификатор пользователя.
    :return: True если пользователь удален и False если пользователь не найден.
    """
    async with async_session_scope() as session:
        user = await get_user_repo(session, user_id, subqueryload(User.subscriptions))
        if user:
            await delete_all_user_subscriptions_repo(session, user)
            await delete_user_repo(session, user)
            return True
        return False


async def get_user(user_id: int) -> User | None:
    """
    Получение информации о регистрации пользователя.

    :param user_id: Идентификатор пользователя
    """
    async with async_session_scope() as session:
        return await get_user_repo(session, user_id)


async def subscription_status(user_id: int, resource_id: str, category_id: str) -> bool:
    """
    Проверяет наличие подписки у пользователя на ресурс.

    :param user_id: Идентификатор пользователя.
    :param resource_id: Идентификатор ресурса.
    :param category_id: Идентификатор категории.
    :return: True если такая подписка есть False если подписки нет.
    """
    async with async_session_scope() as session:
        return bool(await get_subscription_repo(session, user_id, resource_id, category_id))


async def subscribe_user(user_id: int, resource_id: str, category_id: str) -> None:
    """
    Подписывает пользователя на ресурс.

    :param user_id: Идентификатор пользователя.
    :param resource_id: Идентификатор ресурса.
    """
    async with async_session_scope() as session:
        await subscribe_user_repo(session, user_id, resource_id, category_id)


async def unsubscribe_user(user_id: int, resource_id: str, category_id: str) -> None:
    """
    Отменяет подписку пользователя на ресурс.

    :param user_id: Идентификатор пользователя.
    :param resource_id: Идентификатор ресурса.
    :param category_id: Идентификатор категории.
    """
    async with async_session_scope() as session:
        subscription = await get_subscription_repo(session, user_id, resource_id, category_id)
        await delete_subscription_repo(session, subscription)


async def get_news_source(resource_id: str) -> Resource:
    """
    Получение новостного ресурса по id.

    :param resource_id: Идентификатор новостного ресурса.
    :return: Объект Resource.
    """
    async with async_session_scope() as session:
        return await get_news_resource_repo(session, resource_id)


async def get_category_by_id(category_id: str) -> Category:
    """
    Получение категории по id.

    :param category_id: Идентификатор категории.
    :return: Объект Category
    """
    async with async_session_scope() as session:
        return await get_category_by_id_repo(session, category_id)
