import uuid
from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import Row, func, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.constants import NEWS_ACTUAL_TIME
from app.db.models import Category, Resource, User, UserSubscription
from app.db.models.bot import NewsSent
from app.db.models.news_feed import News, NewsRemoteCategory, RemoteCategory
from app.db.tools.sqlalchemy_tools import get_or_create, joinedload_all_relationships
from app.logging import logger


async def register_user_repo(session: AsyncSession, user_id: int) -> bool:
    """
    Регистрация нового пользователя в базе данных.

    :param session:  Объект сессии SQLAlchemy.
    :param user_id:  Идентификатор пользователя.
    :return: True если пользователь зарегистрирован False если он ранее был зарегистрирован.
    """
    _, created = await get_or_create(session, User, user_id=user_id)
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
    Удаляет пользователя из базы данных.

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
    Добавляет новую удаленную категорию если она еще не существует.

    :param session: Объект сессии SQLAlchemy
    :param name: Название категории
    :param url: Ссылка на страницу категории.
    :param news_resource_id: Идентификатор новостного ресурса.
    """
    await get_or_create(session, RemoteCategory, name=name, url=url, news_resource_id=news_resource_id)


async def get_resource_by_url_repo(session: AsyncSession, url: str) -> Resource:
    """
    Получение информации о ресурсе по ссылке.

    :param session: Объект сессии SQLAlchemy.
    :param url: Ссылка по которой необходимо найти ресурс.
    :return: Объект Resource.
    """
    stmt = select(Resource).filter(Resource.url == url)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_resources_for_update_repo(session: AsyncSession, *options) -> Sequence[Resource]:
    """
    Получение списка ресурсов которые необходимо обновить.

    :param session: Объект сессии SQLAlchemy.
    :param options: Опции запроса.
    :return: Список ресурсов для обновления.
    """
    stmt = select(Resource).filter(
        or_(
            Resource.update_datetime + Resource.update_interval < datetime.now(),
            Resource.update_datetime.is_(None),
        )
    )
    if options:
        stmt = stmt.options(*options)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_resource_timeout_repo(session: AsyncSession) -> timedelta:
    """
    Получение времени до ближайшего обновления рессурса.

    :param session:  Объект сессии SQLAlchemy.
    :return: Время в секундах до следующего обновления ресурса.
    """
    stmt = select(
        func.min(func.coalesce((Resource.update_datetime + Resource.update_interval), datetime.now())) - datetime.now()
    )
    result = await session.execute(stmt)
    return result.scalar()


async def get_categories_timeout_repo(session: AsyncSession) -> timedelta:
    """
    Получение времени до ближайшего обновления категории.

    :param session:  Объект сессии SQLAlchemy.
    :return: Время в секундах до следующего обновления категории.
    """
    stmt = select(
        func.min(
            func.coalesce(
                (RemoteCategory.update_datetime + RemoteCategory.update_interval), datetime.now()
            )
        )
        - datetime.now()
    ).where(
        RemoteCategory.parser_id.isnot(None),
        RemoteCategory.category_id.isnot(None),
        or_(
            RemoteCategory.deletion_datetime.is_(None),
            RemoteCategory.deletion_datetime > datetime.now(),
        ),
        or_(
            Category.deletion_datetime.is_(None),
            Category.deletion_datetime > datetime.now(),
        )

    ).join(Category)
    result = await session.execute(stmt)
    return result.scalar()


async def get_categories_for_update_repo(session: AsyncSession, *options) -> Sequence[RemoteCategory]:
    """
    Получение списка категорий для обновления.

    :param session: Объект сессии SQLAlchemy.
    :param options: Опции запроса.
    :return: Список категорий для обновления.
    """
    stmt = select(RemoteCategory).filter(
        RemoteCategory.parser_id.isnot(None),
        RemoteCategory.category_id.isnot(None),
        or_(
            RemoteCategory.deletion_datetime.is_(None),
            RemoteCategory.deletion_datetime > datetime.now(),
        ),
        or_(
            Category.deletion_datetime.is_(None),
            Category.deletion_datetime > datetime.now(),
        ),
        or_(
            RemoteCategory.update_datetime.is_(None),
            RemoteCategory.update_datetime + RemoteCategory.update_interval < datetime.now(),
        )
    ).join(Category)
    if options:
        stmt = stmt.options(*options)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_news_by_url_repo(session: AsyncSession, url: str) -> News | None:
    """
    Получение новости по ссылке.

    :param session:
    :param url:
    :return: Объект новости если он существует None если он не найден.
    """
    stmt = select(News).where(News.news_url == url)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_news_repo(session: AsyncSession, **kwargs) -> News:
    """
    Создание новости.

    :param session: Объект сессии SQLAlchemy.
    :param kwargs: Поля модели News для создания.
    """
    news = News(**kwargs)
    session.add(news)
    return news


async def get_remote_category_by_url_repo(session: AsyncSession, url: str) -> RemoteCategory:
    """
    Получает удаленную категорию по адресу ссылки.

    :param session: Объект сессии SQLAlchemy.
    :param url: Ссылка на страницу категории.
    :return: Объект RemoteCategory.
    """
    stmt = select(RemoteCategory).where(RemoteCategory.url == url)
    result = await session.execute(stmt)
    return result.scalars().first()


async def add_remote_category_to_news_repo(
    session: AsyncSession, remote_category_id: uuid.UUID, news_id: uuid.UUID
) -> None:
    """
    Привязывает к новости удаленную категорию.

    :param session: Объект сессии SQLAlchemy.
    :param remote_category_id: Идентификатор категории
    :param news_id: Идентификатор новости
    """
    await get_or_create(session, NewsRemoteCategory, remote_category_id=remote_category_id, news_id=news_id)


async def get_news_for_send_repo(session: AsyncSession) -> Sequence[Row]:
    """
    Получает новости для отправки подписчикам.

    :param session:
    :return: Список объектов Row (user_id, news_title, news_content, news_date, news_id, news_url)
    """
    stmt = select(
        User.user_id.label('user_id'),
        News.title.label('news_title'),
        News.content.label('news_content'),
        func.coalesce(News.published_at, News.detected_at).label('news_date'),
        News.id.label('news_id'),
        News.news_url.label('news_url'),
    ).select_from(User).distinct().join(
        UserSubscription, UserSubscription.user_id == User.user_id,
    ).join(
        Category, Category.id == UserSubscription.category_id,
    ).join(
        Resource, Resource.id == UserSubscription.resource_id,
    ).join(
        RemoteCategory, (RemoteCategory.category_id == Category.id)
                        & (RemoteCategory.news_resource_id == Resource.id),
    ).join(
        NewsRemoteCategory, NewsRemoteCategory.remote_category_id == RemoteCategory.id,
    ).join(
        News, News.id == NewsRemoteCategory.news_id,
    ).outerjoin(
        NewsSent, (NewsSent.news_id == News.id)
                  & (NewsSent.user_id == User.user_id),
    ).where(
        NewsSent.id.is_(None),
        News.parsed_at > datetime.now() - timedelta(seconds=NEWS_ACTUAL_TIME),
        News.content.isnot(None)
    )
    result = await session.execute(stmt)
    news_tasks = result.all()

    # news_sent = [NewsSent(user_id=task.user_id, news_id=task.news_id) for task in news_tasks]
    # session.add_all(news_sent)

    if news_tasks:
        news_sent = [{'user_id': task.user_id, 'news_id': task.news_id} for task in news_tasks]
        insert_stmt = insert(NewsSent).values(news_sent)
        await session.execute(insert_stmt)
    return news_tasks
