import asyncio
from typing import Type, Dict, Any, Union

from app.db.models import News
from app.parsers import BaseParser

_news_parsing_queue = asyncio.Queue()
_message_queue = asyncio.Queue()

async def add_news_to_parse_queue(news: News, parser_class: Type[BaseParser]) -> None:
    """
    Добавляет объект новости и класс парсера в очередь парсинга.
    :param news: Объект класса News который необходимо спарсить.
    :param parser_class: Класс парсера для парсинга новости.
    """
    await _news_parsing_queue.put({
        'news': news,
        'parser_class': parser_class,
    })


async def get_task_from_news_parse_queue() -> Dict[str, Union[News, Type[BaseParser]]]:
    """
    Получение из очереди для парсинга новостей задачи.
    :return: Словарь содержащий новость и класс парсера
    """
    return await _news_parsing_queue.get()

