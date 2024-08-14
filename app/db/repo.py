import uuid
from typing import Sequence

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, UserSubscription, Resource, Category
from app.db.models.news_feed import RemoteCategory
from app.db.tools.sqlalchemy_tools import get_or_create, joinedload_all_relationships
from app.logging import logger


async def register_user_repo(session: AsyncSession, user_id: int) -> bool:
    """
    Регистрация нового пользователя в базе данных.
    :param session:  Объект сессии SQLAlchemy.
    :param user_id:  Идентификатор пользователя.
    :return: Строка со статусом.
    """
    instance, created = await get_or_create(session, User, user_id=user_id)
    return created


async def get_user_repo(session: AsyncSession, user_id: int, *options, joinedload_all: bool = False) -> User | None:
    """
    Получение пользователя по id.
    :param session:  Объект сессии SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :param options: Опции для запроса.
    :param joinedload_all: Загрузить все связанные таблицы используя joinedload.
    :return: Объект модели User или None если пользователь не найден.
    """
    if options and joinedload_all:
        await logger.warning('Некорректные параметры функции')
        raise ValueError('Нельзя использовать options и joinedload_all одновременно.')
    stmt = select(User).filter(User.user_id == user_id)
    if options:
        stmt = stmt.options(*options)
    if joinedload_all:
        options = joinedload_all_relationships(User)
        stmt = stmt.options(*options)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def delete_all_user_subscriptions_repo(session: AsyncSession, user: User) -> None:
    """
    Удаляет все подписки пользователя.
    :param session: Объект сессии SQLAlchemy.
    :param user: Объект модели Users у которого необходимо удалить подписки.
    """
    if user.subscriptions:
        user.subscriptions.delete()


async def delete_user_repo(session: AsyncSession, user: User) -> None:
    """
    Удаляет пользователя из базы данных
    :param session: Объект сессии SQLAlchemy.
    :param user: Объект модели User который необходимо удалить.
    """
    if user:
        await session.delete(user)


async def get_subscription_repo(session: AsyncSession, user_id: int, resource_id: str) -> UserSubscription:
    """
    Проверяет подписку у пользователя в базе данных.
    :param session: Объект сессии SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :param resource_id: Идентификатор ресурса.
    :return: True если подписка есть False если подписки нет.
    """
    stmt = select(UserSubscription).filter(
        UserSubscription.user_id == user_id, UserSubscription.resource_id == resource_id,
    )
    result = await session.execute(stmt)
    return result.scalar()


async def subscribe_user_repo(session: AsyncSession, user_id: int, resource_id: str) -> None:
    """
    Подписывает пользователя на ресурс.
    :param session: Объект сессии SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :param resource_id: Идентификатор ресурса.
    """
    user_subscription = UserSubscription(user_id=user_id, resource_id=resource_id)
    session.add(user_subscription)


async def delete_subscription_repo(session: AsyncSession, subscription: UserSubscription) -> None:
    """
    Удаляет подписку пользователя на ресурс.
    :param session: Объект сессии SQLAlchemy.
    :param subscription: Объект подписки который необходимо удалить.
    """
    await session.delete(subscription)


async def get_news_resource_repo(session: AsyncSession, resource_id: str) -> Resource:
    """
     Получение информации о новостном ресурсе их базы данных.
    :param session: Объект сессии SQLAlchemy.
    :param resource_id: Идентификатор новостного ресурса.
    :return: Объект Resource.
    """
    stmt = select(Resource).filter(Resource.id == resource_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_news_resources_repo(session: AsyncSession) -> Sequence[Resource]:
    """
    Получение списка источников новостей доступных для подписки из базы данных.
    :param session: Объект сессии SQLAlchemy
    :return: Список объектов Resource
    """
    stmt = select(Resource).order_by(Resource.title)
    result = await session.execute(stmt)
    return result.scalars().all()


async def add_remote_categories_repo(session: AsyncSession, name: str, url: str, news_resource_id: uuid.UUID) -> None:
    """

    :param session: Объект сессии SQLAlchemy
    :param name: Название категории
    :param url: Ссылка на страницу категории.
    :param news_resource_id: Идентификатор новостного ресурса.
    """
    await get_or_create(session, RemoteCategory, name=name, url=url, news_resource_id=news_resource_id)
