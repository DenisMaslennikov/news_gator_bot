from typing import List

from selenium.webdriver.common.by import By

from .base import AsyncSeleniumParser

class YandexNewsCategoriesParser(AsyncSeleniumParser):
    """Парсер категорий с яндекс новостей."""

    async def parse(self) -> None:
        """Парсер списка категорий яндекс новостей."""
        categories_xpath = 'news-rubricator'
        categories_list = self._driver.find_element(By.CLASS_NAME, categories_xpath).find_elements(By.TAG_NAME, 'a')
        categories = [
            {
                'name': category.text,
                'url': category.get_attribute('href'),
            }
            for category in categories_list
        ]
        self.categories = categories
