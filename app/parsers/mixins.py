import asyncio
import datetime

from sqlalchemy.orm import joinedload

import app.parsers
from app.db.models import Resource
from app.db.models.news_feed import RemoteCategory
from app.db.repo import (
    add_remote_categories_repo,
    add_remote_category_to_news_repo,
    create_news_repo,
    get_news_by_url_repo,
    get_remote_category_by_url_repo,
    get_resource_by_url_repo,
)
from app.db.session import async_session_scope
from app.logging import logger
from app.queue import add_task_to_parse_queue


class CategoryProcessDataMixin:
    """Сохранение спарсеных категорий в базу данных."""

    async def process_data(self) -> None:
        """Обновляет спарсенные данные в базе данных."""
        await logger.debug(f'Сохраняю спарсенные c {self.url} данные в базе данных')
        async with async_session_scope() as session:
            resource = await get_resource_by_url_repo(session, self.url)
            for category in self.categories:
                await add_remote_categories_repo(session, **category, resource_id=resource.id)
            resource.update_datetime = datetime.datetime.now()


class NewsContentProcessDataMixin:
    """Сохранение спарсеной новости в базу данных."""

    async def process_data(self) -> None:
        """Сохранение спарсенной новости в базу данных."""
        if hasattr(self, 'content') and self.content:
            await logger.debug(f'Сохраняем спарсенную новость в базу {self.url}')
            async with async_session_scope() as session:
                news = await get_news_by_url_repo(session, self.url)
                news.content = self.content
                news.parsed_at = datetime.datetime.now()
                news.published_at = getattr(self, 'published_at', None)
                # images = getattr(self, 'images', None)
        else:
            await logger.debug(f'Контент не получен нечего сохранять в бд {self.url}')


class NewsListProcessDataMixin:
    """Миксин обработки списка новостей."""
    lock = asyncio.Lock()

    async def process_data(self) -> None:
        """Сохранение спаршенных данных о новостях."""
        await logger.debug(f'Сохраняем спарсенные c {self.url} данные')
        news_list = []
        async with self.lock:
            async with async_session_scope() as session:
                remote_category = await get_remote_category_by_url_repo(
                    session,
                    self.url,
                    joinedload(RemoteCategory.resource).joinedload(Resource.detailed_parser)
                )
                for index in range(len(self.urls)):
                    news = await get_news_by_url_repo(session, self.urls[index])
                    if not news:
                        news = await create_news_repo(
                            session,
                            title=self.titles[index],
                            news_url=self.urls[index],
                            description=self.descriptions[index],
                            detected_at=datetime.datetime.now(),
                        )
                        news_list.append(news)
                        await session.flush()
                    await add_remote_category_to_news_repo(session, remote_category.id, news.id)
        for news in news_list:
            try:
                await add_task_to_parse_queue(news.news_url, getattr(
                    app.parsers, remote_category.resource.detailed_parser.parser_class
                ), remote_category.resource.id)
            except AttributeError:
                logger.warning(f'Парсер {remote_category.resource.detailed_parser.parser_class} не найден')
                # TODO отправка сообщения в телеграм
