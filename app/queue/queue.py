import asyncio
from typing import Dict, Type, Union

from app.parsers import BaseParser

_parsing_queue = asyncio.Queue()
_message_queue = asyncio.Queue()


async def add_task_to_parse_queue(url: str, parser_class: Type[BaseParser]) -> None:
    """
    Добавляет страницу и класс парсера в очередь парсинга.

    :param url: URL страницы которую необходимо спарсить.
    :param parser_class: Класс парсера для парсинга новости.
    """
    await _parsing_queue.put({
        'url': url,
        'parser_class': parser_class,
    })


async def get_task_from_parse_queue() -> Dict[str, Union[str, Type[BaseParser]]]:
    """
    Получение из очереди для парсинга задачи.

    :return: Словарь содержащий url и класс парсера
    """
    return await _parsing_queue.get()
