from typing import List

from selenium.webdriver.common.by import By

from .base import AsyncSeleniumParser
from ..db.repo import add_remote_categories_repo
from ..db.session import session_scope


class YandexNewsCategoriesParser(AsyncSeleniumParser):
    """Парсер категорий с яндекс новостей."""

    async def parse(self) -> None:
        """Парсер списка категорий яндекс новостей."""
        categories_class_name = 'news-rubricator'
        categories_list = self._driver.find_element(
            By.CLASS_NAME, categories_class_name
        ).find_elements(By.TAG_NAME, 'a')
        categories = [
            {
                'name': category.text,
                'url': category.get_attribute('href'),
            }
            for category in categories_list
        ]
        self.categories = categories

    async def proces_data(self) -> None:
        """Обновляет спарсенные данные в базе данных."""
        async with session_scope() as session:
            for category in self.categories:
                await add_remote_categories_repo(session, **category, **self.extra_data)
