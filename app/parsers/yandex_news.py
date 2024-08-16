import datetime
from urllib.parse import urlsplit

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from .base import AsyncSeleniumParser
from ..db.repo import add_remote_categories_repo, get_resource_by_url_repo, get_news_by_url_repo, create_news_repo, \
    get_remote_category_by_url_repo
from ..db.session import session_scope
from ..logging import logger
from ..queue import add_news_to_parse_queue


class YandexNewsMainPageParser(AsyncSeleniumParser):
    """Парсер категорий с яндекс новостей."""

    def parse(self) -> None:
        """Парсер списка категорий яндекс новостей."""
        logger.debug('Распарсиваю главную страницу яндекс новостей')
        categories_class_name = 'news-rubricator'
        categories_list = self._driver.find_element(
            By.CLASS_NAME, categories_class_name
        ).find_elements(By.TAG_NAME, 'a')
        self.categories  = [
            {
                'name': category.text,
                'url': category.get_attribute('href'),
            }
            for category in categories_list
        ]
        logger.debug(f'Получен список категорий с яндекса')
        if not self.categories:
            logger.warning(f'Не удалось получить список категорий с яндекс новостей {self.__class__}')
            # TODO добавить отправку сообщения администратору


    async def proces_data(self) -> None:
        """Обновляет спарсенные данные в базе данных."""
        await logger.debug('Сохраняю спарсенные данные в базе данных')
        async with session_scope() as session:
            resource = await get_resource_by_url_repo(session, self.url)
            for category in self.categories:
                await add_remote_categories_repo(session, **category, news_resource_id=resource.id)
            resource.update_datetime = datetime.datetime.now()


class YandexNewsDetailParser(AsyncSeleniumParser):
    """Парсер детальной информации о новости."""

    def parse(self) -> None:
        """Парсит детальную информацию о новости"""
        logger.debug(f'Парсим новость с яндекса {self.url}')
        try:
            block_css_selector = "[class^='news-story-'][class$='__body']"
            block = self._driver.find_element(By.CSS_SELECTOR, block_css_selector)
            news_block_css_selector = "[class^='news-story-'][class$='__summarization-item']"
            news_blocks = block.find_elements(By.CSS_SELECTOR, news_block_css_selector)
            content = ''
            for news_block in news_blocks:
                content += news_block.find_element(By.TAG_NAME, 'span').text
                url_block = news_block.find_element(By.TAG_NAME, 'a')
                split_url = urlsplit(url_block.get_attribute('href'))
                url = f'{split_url.scheme}://{split_url.netloc}{split_url.path}'
                content += f'\n<a href="{url}">{url_block.text}</a>\n'

            self.content = content
        except NoSuchElementException as e:
            logger.warning(f'Ошибка парсинга страницы {self.url} новость не найдена')

    async def proces_data(self) -> None:
        """Сохранение спарсенной новости в базу данных."""
        if self.content:
            await logger.debug(f'Сохраняем спарсенную новость в базу {self.url}')
            async with session_scope() as session:
                news = await get_news_by_url_repo(session, self.url)
                news.content = self.content
        else:
            await logger.debug(f'Контент не получен нечего сохранять в бд {self.url}')


class YandexNewsCategoryParser(AsyncSeleniumParser):
    """Парсер категорий яндекс новостей без подкатегорий."""

    def parse(self) -> None:
        """Парсим новости со страницы категории без подкатегорий."""
        logger.debug(f'Распарсиваем страницу категории {self.url}')
        news_feed_class_name = 'Feed-desktop__list-3q'
        news_feed_block = self._driver.find_element(By.CLASS_NAME, news_feed_class_name)
        news_block_css_selector = ".mg-card__shown-card[class*='news-card2-'][class*='__show-']"
        description_css_selector = "[class^='news-card2-'][class$='__annotation']"
        title_css_selector = "[class^='news-card2-'][class$='__title']"
        news_blocks = news_feed_block.find_elements(By.CSS_SELECTOR, news_block_css_selector )
        images_urls = []
        titles = []
        descriptions = []
        urls = []
        for news_block in news_blocks:
            images_urls.append(news_block.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            descriptions.append(news_block.find_element(By.CSS_SELECTOR, description_css_selector).text)
            titles.append(news_block.find_element(By.CSS_SELECTOR, title_css_selector).text)
            url_block = news_block.find_element(By.TAG_NAME, 'a')
            split_url = urlsplit(url_block.get_attribute('href'))
            urls.append(f'{split_url.scheme}://{split_url.netloc}{split_url.path}')
        self.descriptions = descriptions
        self.titles = titles
        self.urls = urls
        self.images_urls = images_urls
        if not all([descriptions, titles, urls, images_urls]):
            logger.warning(f'Ошибка парсинга категории {self.url} парсером {self.__class__} получены не все данные')

    async def proces_data(self) -> None:
        """Сохранение спаршенных данных о новостях"""
        logger.debug(f'Сохраняем спарсенные c {self.url} данные')
        async with session_scope() as session:
            remote_category = await get_remote_category_by_url_repo(session, self.url)
            for index in range(len(self.urls)):
                news = await get_news_by_url_repo(session, self.urls[index])
                if news:
                    continue
                news = await create_news_repo(
                    session,
                    title=self.titles[index],
                    news_url=self.urls[index],
                    description=self.descriptions[index],
                    detected_at=datetime.datetime.now(),
                )
                await add_news_to_parse_queue(news, YandexNewsDetailParser)
            remote_category.update_datetime = datetime.datetime.now()
