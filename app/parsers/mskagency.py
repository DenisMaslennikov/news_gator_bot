import re

from bs4 import BeautifulSoup

from app.logging import logger
from app.parsers.base import aiohttpParser
from app.parsers.mixins import NewsListProcessDataMixin


class MskagencyMainPageParser(NewsListProcessDataMixin, aiohttpParser):
    """Парсер списка новостей с сайта агентства городских новостей Москва."""

    def parse(self) -> None:
        """Парсит главную страницу агенства городских новостей Москва."""
        if hasattr(self, '_data') and self._data is not None:
            logger.debug('Распарсиваем главную страницу Агентства городских новостей Москва')
            soup = BeautifulSoup(self._data, 'lxml')
            block = soup.select_one('div.NewsList.js-NewsList__all')
            print(block)
            news_blocks = block.find_all('div', class_=re.compile(r'^MaterialRow\d$'))
            print(news_blocks)
        else:
            logger.debug(f'Нет данных для {self.url} нечего парсить')

    async def process_data(self) -> None:
        """Заглушка."""
        pass
