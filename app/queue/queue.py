import asyncio
import datetime
import uuid
from collections import namedtuple
from typing import Type

_parsing_queue = asyncio.Queue()
_message_queue = asyncio.Queue()

MessageTask = namedtuple('MessageTask', [
    'user_id', 'news_title', 'news_content', 'news_date', 'news_id', 'news_url',
])

ParsingTask = namedtuple('ParsingTask', ['url', 'parser_class', 'resource_id'])


async def add_task_to_parse_queue(url: str, parser_class, resource_id: uuid.UUID) -> None:
    """
    Добавляет страницу и класс парсера в очередь парсинга.

    :param url: URL страницы которую необходимо спарсить.
    :param parser_class: Класс парсера для парсинга новости.
    """
    await _parsing_queue.put(ParsingTask(url, parser_class, resource_id))


async def get_task_from_parse_queue() -> ParsingTask:
    """
    Получение из очереди для парсинга задачи.

    :return: Объект содержащий url и класс парсера.
    """
    return await _parsing_queue.get()


async def add_task_to_message_queue(
    user_id: int,
    news_title: str,
    news_content: str,
    news_date: datetime.datetime,
    news_id: uuid.UUID,
    news_url: str,
) -> None:
    """
    Добавляет задачу отправки сообщений в очередь задач.

    :param user_id: Идентификатор пользователя - получателя.
    :param news_title: Заголовок новости.
    :param news_content: Содержимое новости.
    :param news_date: Дата новости.
    :param news_id: Идентификатор новости.
    :param news_url: Ссылка на оригинальную новость на сайте источника.
    """
    task = MessageTask(
        user_id=user_id,
        news_title=news_title,
        news_content=news_content,
        news_date=news_date,
        news_id=news_id,
        news_url=news_url,
    )
    await _message_queue.put(task)


async def get_task_from_message_queue() ->  MessageTask:
    """
    Получение из очереди для отправки сообщений задачи.

    :return: Объект MessageTask с полями ('user_id', 'news_title', 'news_content', 'news_date', 'news_id', 'news_url')
    """
    return await _message_queue.get()
