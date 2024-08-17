import asyncio
import datetime
from urllib.parse import urlsplit

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from .base import AsyncSeleniumParser
from app.db.repo import add_remote_categories_repo, get_resource_by_url_repo, get_news_by_url_repo, create_news_repo, \
    get_remote_category_by_url_repo, add_remote_category_to_news_repo
from app.db.session import session_scope
from app.logging import logger
from app.queue import add_task_to_parse_queue


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
        if hasattr(self, 'content') and self.content:
            await logger.debug(f'Сохраняем спарсенную новость в базу {self.url}')
            async with session_scope() as session:
                news = await get_news_by_url_repo(session, self.url)
                news.content = self.content
        else:
            await logger.debug(f'Контент не получен нечего сохранять в бд {self.url}')

class YandexNewsCategoryBaseParser(AsyncSeleniumParser):
    """Базовый парсер категорий яндекса."""
    lock = asyncio.Lock()

    async def proces_data(self) -> None:
        """Сохранение спаршенных данных о новостях"""
        logger.debug(f'Сохраняем спарсенные c {self.url} данные')

        async with self.lock:
            async with session_scope() as session:
                remote_category = await get_remote_category_by_url_repo(session, self.url)
                for index in range(len(self.urls)):
                    news = await get_news_by_url_repo(session, self.urls[index])
                    if not news:
                        news = await create_news_repo(
                            session,
                            title=self.titles[index],
                            news_url=self.urls[index],
                            description=self.descriptions[index],
                            detected_at=datetime.datetime.now(),
                        )
                        await add_task_to_parse_queue(news.news_url, YandexNewsDetailParser)
                        await session.flush()
                    await add_remote_category_to_news_repo(session, remote_category.id, news.id)


class YandexNewsCategoryParser(YandexNewsCategoryBaseParser):
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
            try:
                images_urls.append(news_block.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            except NoSuchElementException:
                images_urls.append(None)
                logger.debug(f'Не найдено изображение для новости')
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
            # TODO Добавить сообщение


class YandexNewsCategoryWithSubCategoriesParser(YandexNewsCategoryBaseParser):
    """Парсер категорий яндекс новостей без подкатегорий."""

    def parse(self) -> None:
        """Парсим новости со страницы категории без подкатегорий."""
        logger.debug(f'Распарсиваем страницу категории {self.url}')
        titles = []
        urls = []
        descriptions = []
        images_urls = []
        left_block_css_selector = '.news-layout-column-redesign__col.news-top-stories__top'
        left_block = self._driver.find_element(By.CSS_SELECTOR, left_block_css_selector)
        left_news_blocks = left_block.find_elements(By.TAG_NAME, 'article')

        for block in left_news_blocks:
            titles.append(block.find_element(By.CLASS_NAME, 'card-part-news-title__title-3m').text)
            try:
                images_urls.append(block.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            except NoSuchElementException:
                images_urls.append(None)
                logger.debug('Не найдено изображение для новости')
            descriptions.append(
                block.find_element(
                    By.CSS_SELECTOR,
                    ".card-part-news-description__description-3W[class*='card-part-news-description__line-']"
                ).text
            )
            url = block.find_element(
                By.CSS_SELECTOR,
                '.card-part-content-wrapper__contentWrapper-27.card-part-content-wrapper__news-1l'
            ).find_element(By.TAG_NAME, 'a').get_attribute('href')
            split_url = urlsplit(url)
            urls.append(f'{split_url.scheme}://{split_url.netloc}{split_url.path}')
        right_block_css_class_name = 'news-top-stories__others-inner'
        right_block = self._driver.find_element(By.CLASS_NAME, right_block_css_class_name)
        right_news_blocks = right_block.find_elements(By.CLASS_NAME, 'news-top-stories__other')
        for block in right_news_blocks:
            titles.append(block.find_element(By.TAG_NAME, 'p').text)
            images_urls.append(None)
            descriptions.append(None)
            url = block.find_element(By.TAG_NAME, 'a').get_attribute('href')
            split_url = urlsplit(url)
            urls.append(f'{split_url.scheme}://{split_url.netloc}{split_url.path}')
        down_block_css_class_name = 'Feed-desktop__list-3q'
        down_block = self._driver.find_element(By.CLASS_NAME, down_block_css_class_name)
        down_news_blocks = down_block.find_elements(
            By.CSS_SELECTOR, '.mg-card__shown-card.CardHorizontal__showCardWrapper-1t'
        )
        for block in down_news_blocks:
            url = block.find_element(By.TAG_NAME, 'a').get_attribute('href')
            split_url = urlsplit(url)
            urls.append(f'{split_url.scheme}://{split_url.netloc}{split_url.path}')
            titles.append(block.find_element(By.CLASS_NAME, 'news-card2-redesign__title').text)
            descriptions.append(block.find_element(By.CLASS_NAME, 'news-card2-redesign__annotation').text)
            try:
                images_urls.append(block.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            except NoSuchElementException:
                images_urls.append(None)
                logger.debug('Изображение к новости не найдено')
        self.titles = titles
        self.urls = urls
        self.images_urls = images_urls
        self.descriptions = descriptions
