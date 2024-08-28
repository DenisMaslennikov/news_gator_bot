import asyncio
import random
import uuid
from datetime import datetime, timedelta
from typing import Type

import fake_useragent
from sqlalchemy.orm import joinedload

import app.parsers
from app.config.constants import MAX_SELENIUM_TASKS, MAX_AIOHTTP_TASKS
from app.db.models import Resource
from app.db.models.news_feed import RemoteCategory
from app.db.repo import (
    get_categories_for_update_repo,
    get_categories_timeout_repo,
    get_resource_timeout_repo,
    get_resources_for_update_repo, get_parser_limits_repo,
)
from app.db.session import async_session_scope, session_scope
from app.logging import logger
from app.parsers.base import BaseParser, ThreadSeleniumParser, aiohttpParser
from app.queue import get_task_from_parse_queue, add_task_to_parse_queue

with session_scope() as session:
    # Получаем лимиты для парсеров в зависимости от ресурса.
    resources_with_limits = get_parser_limits_repo(session)
    limits ={resource.resource_id: {
        'semaphore': asyncio.Semaphore(resource.task_limit),
        'sleep_timeout': resource.sleep_timout,
    }

    for resource in resources_with_limits}


selenium_semaphore = asyncio.Semaphore(MAX_SELENIUM_TASKS)
aiohttp_semaphore = asyncio.Semaphore(MAX_AIOHTTP_TASKS)


def get_parser(parser_name: str) -> Type[BaseParser] | None:
    """
    Получает класс парсера по названию.

    :param parser_name: Название класса парсера.
    :return: Класс парсера по названию.
    """
    try:
        parser_class = getattr(app.parsers, parser_name)
    except AttributeError:
        logger.warning(f'Неизвестный класс парсера {parser_name}')
        parser_class = None
        # TODO Добавить отправку сообщения
    return parser_class


async def create_resource_parse_tasks() -> None:
    """Создание задач для парсинга ресурсов."""
    async with async_session_scope() as session:
        resources_for_update = await get_resources_for_update_repo(session, joinedload(Resource.parser))

        for resource in resources_for_update:
            resource.update_datetime = datetime.now()
            await add_task_to_parse_queue(resource.url, get_parser(resource.parser.parser_class), resource.id)


async def create_category_parse_tasks() -> None:
    """Создание задач для парсинга категорий."""
    async with async_session_scope() as session:
        categories_for_update = await get_categories_for_update_repo(session, joinedload(RemoteCategory.parser))

        for category in categories_for_update:
            category.update_datetime = datetime.now() + timedelta(
                seconds=random.randint(0, 2 * int(category.update_interval.total_seconds()))
            )
            await add_task_to_parse_queue(category.url, get_parser(category.parser.parser_class), category.resource_id)


async def parse_resources_loop() -> None:
    """Цикл создания заданий парсинга ресурсов."""
    while True:
        async with async_session_scope() as session:
            sleep_interval = (await get_resource_timeout_repo(session)).total_seconds()
            if sleep_interval < 0:
                sleep_interval = 0
        await logger.debug(f'Парсер ресурсов спит {sleep_interval} секунд')
        await asyncio.sleep(sleep_interval)
        await create_resource_parse_tasks()


async def parse_categories_loop() -> None:
    """Цикл задач парсинга категорий."""
    while True:
        async with async_session_scope() as session:
            sleep_interval = (await get_categories_timeout_repo(session)).total_seconds()
            if sleep_interval < 0:
                sleep_interval = 0
            await logger.debug(f'Парсер категорий спит {sleep_interval} секунд')
            await asyncio.sleep(sleep_interval)
            await create_category_parse_tasks()


async def create_parse_task(url: str, parser_class: Type[BaseParser], resource_id: uuid.UUID) -> None:
    """
    Создает асинхронную таску парсинга новости.

    :param url: Ссылка которую необходимо спарсить.
    :param parser_class: Класс парсера.
    """
    loop = asyncio.get_running_loop()
    loop.create_task(_parse_task(parser_class, url, resource_id))


async def parse_queue_loop() -> None:
    """Цикл парсинга новостей из очереди."""
    while True:
        await logger.debug('Жду задачу парсинга')
        task = await get_task_from_parse_queue()
        await logger.debug(f'создаю таску для парсинга по адресу {task.url}')
        await create_parse_task(task.url, task.parser_class, task.resource_id)


async def _parse_task(parser_class: Type[BaseParser], url: str, resource_id: uuid.UUID) -> None:
    """
    Обработчик задачи парсинга.

    :param parser_class: Класс парсера для обработки url.
    :param url: Ссылка которую необходимо спарсить.

    """
    if limits.get(resource_id) is not None:
        await limits.get(resource_id).get('semaphore').acquire()
    if issubclass(parser_class, ThreadSeleniumParser):
        await selenium_semaphore.acquire()
    if issubclass(parser_class, aiohttpParser):
        await aiohttp_semaphore.acquire()
    try:
        parse = parser_class(url, fake_useragent.UserAgent(browsers='chrome', platforms='pc').random)
        await parse.fetch_data()
        await asyncio.sleep(0)
        parse.parse()
        await parse.process_data()
    finally:
        if limits.get(resource_id) is not None:
            await asyncio.sleep(limits.get(resource_id).get('sleep_timeout'))
            limits.get(resource_id).get('semaphore').release()
        if issubclass(parser_class, ThreadSeleniumParser):
            parse.close()
            selenium_semaphore.release()
        if issubclass(parser_class, aiohttpParser):
            aiohttp_semaphore.release()

