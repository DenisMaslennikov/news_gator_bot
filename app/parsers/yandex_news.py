from urllib.parse import urlsplit

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from app.logging import logger

from .base import ThreadSeleniumParser
from .mixins import CategoryProcessDataMixin, NewsContentProcessDataMixin, NewsListProcessDataMixin


class YandexNewsMainPageParser(CategoryProcessDataMixin, ThreadSeleniumParser):
    """Парсер категорий с яндекс новостей."""

    def parse(self) -> None:
        """Парсер списка категорий яндекс новостей."""
        logger.debug('Распарсиваю главную страницу яндекс новостей')
        categories_class_name = 'news-rubricator'
        categories_list = self._driver.find_element(
            By.CLASS_NAME, categories_class_name
        ).find_elements(By.TAG_NAME, 'a')
        self.categories = [
            {
                'name': category.text,
                'url': category.get_attribute('href'),
            }
            for category in categories_list
        ]
        logger.debug('Получен список категорий с яндекса')
        if not self.categories:
            logger.warning(f'Не удалось получить список категорий с яндекс новостей {self.__class__}')
            # TODO добавить отправку сообщения администратору


class YandexNewsDetailParser(NewsContentProcessDataMixin, ThreadSeleniumParser):
    """Парсер детальной информации о новости."""

    def parse(self) -> None:
        """Парсит детальную информацию о новости."""
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
        except NoSuchElementException:
            logger.warning(f'Ошибка парсинга страницы {self.url} новость не найдена')


class YandexNewsCategoryParser(NewsListProcessDataMixin, ThreadSeleniumParser):
    """Парсер категорий яндекс новостей без подкатегорий."""

    def parse(self) -> None:
        """Парсим новости со страницы категории без подкатегорий."""
        logger.debug(f'Распарсиваем страницу категории {self.url}')
        news_feed_class_name = 'news-site--Feed-desktop__list-3q'
        news_feed_block = self._driver.find_element(By.CLASS_NAME, news_feed_class_name)
        news_block_css_selector = '.news-site--ShownCard__shownCard-1f'
        description_css_selector = '.news-card__annotation'
        title_css_selector = '.news-card__title'
        news_blocks = news_feed_block.find_elements(By.CSS_SELECTOR, news_block_css_selector)
        images_urls = []
        titles = []
        descriptions = []
        urls = []
        if not news_blocks:
            logger.warning(f'Блок с новостями не найден {self.url}')
        for news_block in news_blocks:
            try:
                images_urls.append(news_block.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            except NoSuchElementException:
                images_urls.append(None)
                logger.debug('Не найдено изображение для новости')
            try:
                descriptions.append(news_block.find_element(By.CSS_SELECTOR, description_css_selector).text)
            except NoSuchElementException:
                logger.warning(f'Не найден дескрипшен к новости {self.url}')
            try:
                titles.append(news_block.find_element(By.CSS_SELECTOR, title_css_selector).text)
            except NoSuchElementException:
                logger.warning(f'Не найден тайтл к новости {self.url}')
                logger.warning(news_block.get_attribute('outerHTML'))
                break
            url_block = news_block.find_element(By.TAG_NAME, 'a')
            split_url = urlsplit(url_block.get_attribute('href'))
            urls.append(f'{split_url.scheme}://{split_url.netloc}{split_url.path}')
        self.descriptions = descriptions
        self.titles = titles
        self.urls = urls
        self.images_urls = images_urls
        if not all([descriptions, titles, urls, images_urls]):
            logger.warning(f'Ошибка парсинга категории {self.url} парсером {self.__class__} получены не все данные')
            if not descriptions:
                logger.warning('Не получено описание')
            if not titles:
                logger.warning('Не получены заголовки')
            if not urls:
                logger.warning('Не получены ссылки')
            if not images_urls:
                logger.warning('Не получены изображения')
            # TODO Добавить сообщение


class YandexNewsCategoryWithSubCategoriesParser(NewsListProcessDataMixin, ThreadSeleniumParser):
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
            titles.append(block.find_element(By.CLASS_NAME, 'news-site--card-part-news-title__title-3m').text)
            try:
                images_urls.append(block.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            except NoSuchElementException:
                images_urls.append(None)
                logger.debug('Не найдено изображение для новости')
            descriptions.append(
                block.find_element(
                    By.CSS_SELECTOR,
                    ".news-site--card-part-news-description__description-3W[class*='news-site--card-part-news-descript"
                    "ion__line-']"
                ).text
            )
            url = block.find_element(
                By.CSS_SELECTOR,
                '.news-site--card-part-content-wrapper__contentWrapper-27.news-site--card-part-content-wrapper__news-1l'
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
        down_block_css_class_name = 'news-site--Feed-desktop__list-3q'
        down_block = self._driver.find_element(By.CLASS_NAME, down_block_css_class_name)

        down_news_blocks = down_block.find_elements(
            By.CSS_SELECTOR, '.mg-card__shown-card[class*="news-card2-redesign__show-"]'
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
