import datetime
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.logging import logger
from app.parsers.base import aiohttpParser
from app.parsers.mixins import CategoryProcessDataMixin, NewsContentProcessDataMixin, NewsListProcessDataMixin


class RIANewsMainPageParser(CategoryProcessDataMixin, aiohttpParser):
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


class RIANewsDetailParser(NewsContentProcessDataMixin, aiohttpParser):
    """Парсим детальную информацию о новости с сайта РИА Новостей."""

    def parse(self) -> None:
        """Парсим детальную информацию о новости с сайта РИА Новостей."""
        if hasattr(self, '_data') and self._data is not None:
            logger.debug(f'Парсим новость с РИА новостей {self.url}')
            soup = BeautifulSoup(self._data, 'lxml')
            self.published_at = datetime.datetime.strptime(
                soup.select_one('div.article__info-date').find('a').text.strip(), '%H:%M %d.%m.%Y'
            )
            block = soup.find('div', class_=re.compile(r'layout-article__\d*-align'))
            self.content = block.select_one('div.article__body.js-mediator-article.mia-analytics').text


        else:
            logger.debug(f'Нет данных для {self.url} нечего парсить')

class RIANewsCategoryParser(NewsListProcessDataMixin, aiohttpParser):
    """Парсер списка новостей со страницы категории РИА Новостей."""

    def parse(self) -> None:
        if hasattr(self, '_data') and self._data is not None:
            logger.debug(f'Парсим новости с категории РИА новостей {self.url}')
            soup = BeautifulSoup(self._data, 'lxml')
            block = soup.select_one('div.rubric-list')

            news_blocks = block.find_all('div', class_='list-item__content')
            urls = []
            titles = []
            descriptions = []
            images_urls = []
            for news_block in news_blocks:
                urls.append(news_block.find('a').get('href'))
                titles.append(news_block.select_one('a.list-item__title.color-font-hover-only').text)
                descriptions.append(None)
                try:
                    images_urls.append(news_block.find('img').get('src'))
                except AttributeError:
                    images_urls.append(None)
                    logger.debug(f'Изображение к новости не найдено {self.url}')
            self.urls = urls
            self.titles = titles
            self.descriptions = descriptions
            self.images_urls = images_urls
        else:
            logger.debug(f'Нет данных для {self.url} нечего парсить')

