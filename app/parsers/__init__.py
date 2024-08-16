from typing import Type

from .base import BaseParser
from .yandex_news import YandexNewsMainPageParser, YandexNewsCategoryParser

__all__ = [
    'YandexNewsMainPageParser',
    'YandexNewsCategoryParser',
]
