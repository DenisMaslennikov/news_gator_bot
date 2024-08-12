from typing import List

from selenium.webdriver.common.by import By

from .base import AsyncSeleniumParser

class YandexNewsCategoriesParser(AsyncSeleniumParser):
    """Парсер категорий с яндекс новостей."""

    async def parse(self) -> str | List[str]:
        """Парсет список категорий"""
        body = self._driver.find_element(By.TAG_NAME, 'body')
        categories_xpath = 'news-rubricator'
        categories_list = self._driver.find_element(By.CLASS_NAME, categories_xpath).find_elements(By.TAG_NAME, 'a')
        categories_names = [category.text for category in categories_list]
        print(categories_names)
        #print(body.text)
        return body.text

