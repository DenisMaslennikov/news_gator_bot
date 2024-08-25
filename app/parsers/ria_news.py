from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.logging import logger
from app.parsers.base import aiohttpParser
from app.parsers.mixins import ProcesCategoryDataMixin


class RIANewsMainPageParser(ProcesCategoryDataMixin, aiohttpParser):
    """Парсер списка категорий с сайта РИА Новости."""

    def parse(self) -> None:
        """Парсит главную страницу РИА Новости и ищет названия и ссылки на категории."""
        if hasattr(self, '_data') and self._data is not None:
            logger.debug('Распарсиваем главную страницу Агентства городских новостей Москва')
            soup = BeautifulSoup(self._data, 'lxml')
            block = soup.select_one('div.cell-extension__table')
            categories_blocks = block.find_all('div', class_=['cell-extension__item', 'm-with-title'])
            categories = [{
                'url': urljoin(self.url, category_block.find('a').get('href')),
                'name': category_block.text,
            }
                for category_block in categories_blocks
            ]
            self.categories = categories

        else:
            logger.debug(f'Нет данных для {self.url} нечего парсить')
