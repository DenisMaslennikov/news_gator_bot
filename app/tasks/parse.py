import asyncio

from sqlalchemy.orm import joinedload

import app.parsers
from typing import Type

import fake_useragent

from app.db.models import Resource
from app.db.models.news_feed import RemoteCategory, News
from app.db.repo import get_resources_for_update_repo, get_resource_timeout_repo, get_categories_timeout_repo, \
    get_categories_for_update_repo
from app.db.session import session_scope
from app.logging import logger
from app.parsers.base import BaseParser
from app.queue import get_task_from_news_parse_queue


def get_parser(parser_name: str) -> Type[BaseParser]:
    """
    Получает класс парсера по названию.
    :param parser_name: Название класса парсера.
    :return: Класс парсера по названию.
    """
    parser_class = getattr(app.parsers, parser_name)
    if not parser_class:
        logger.warning(f'Неизвестный класс парсера {parser_name}')
        # TODO Добавить отправку сообщения
    return parser_class


async def create_resource_parse_tasks() -> None:
    """Создание задач для парсинга ресурсов."""
    loop = asyncio.get_running_loop()
    async with session_scope() as session:
        resources_for_update = await get_resources_for_update_repo(session, joinedload(Resource.parser))

    for resource in resources_for_update:
        await loop.create_task(_parse_task(get_parser(resource.parser.parser_class), resource.url))


async def create_category_parse_tasks() -> None:
    """Создание задач для парсинга категорий."""
    loop = asyncio.get_running_loop()
    async with session_scope() as session:
        categories_for_update = await get_categories_for_update_repo(session, joinedload(RemoteCategory.parser))

    for category in categories_for_update:
        await loop.create_task(_parse_task(get_parser(category.parser.parser_class), category.url))


async def parse_resources_loop() -> None:
    """Цикл создания заданий парсинга ресурсов."""
    while True:
        async with session_scope() as session:
            sleep_interval = (await get_resource_timeout_repo(session)).total_seconds()
            if sleep_interval < 0:
                sleep_interval = 0
        await logger.debug(f'Парсер ресурсов спит {sleep_interval} секунд')
        await asyncio.sleep(sleep_interval)
        await create_resource_parse_tasks()


async def parse_categories_loop() -> None:
    """Цикл задач парсинга категорий."""
    while True:
        async with session_scope() as session:
            sleep_interval = (await get_categories_timeout_repo(session)).total_seconds()
            if sleep_interval < 0:
                sleep_interval = 0
            await logger.debug(f'Парсер категорий спит {sleep_interval} секунд')
            await asyncio.sleep(sleep_interval)
            await create_category_parse_tasks()


async def create_news_parse_task(news: News, parser_class: Type[BaseParser]) -> None:
    """
    Создает асинхронную таску парсинга новости.
    :param news: Объект новостей.
    :param parser_class: Класс парсера.
    """
    loop = asyncio.get_running_loop()
    await loop.create_task(_parse_task(parser_class, news.news_url))


async def parse_news_queue_loop() -> None:
    """Цикл парсинга новостей из очереди."""
    while True:
        await logger.debug('Жду задачу парсинга новости')
        task = await get_task_from_news_parse_queue()
        await logger.debug(f'создаю таску для парсинга новости по адресу {task["news"].news_url}')
        await create_news_parse_task(task['news'], task['parser_class'])


async def _parse_task(parser_class: Type[BaseParser], url: str):
    """
    Обработчик задачи парсинга.
    :param parser_class: Класс парсера для обработки url.
    :param url: Сылка которую необходимо спарсить.
    """
    parse = parser_class(url, fake_useragent.UserAgent(browsers='chrome', platforms='pc').random)
    await parse.fetch_data()
    parse.parse()
    await parse.proces_data()
