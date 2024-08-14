import asyncio
import os
import traceback
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import List, AsyncContextManager

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from app.config.constants import CHROME_BINARY_LOCATION, CHROMEDRIVER_LOCATION


class BaseParser(ABC):
    """Базовый класс парсера."""

    def __init__(self, url: str, user_agent: str, *args, **kwargs) -> None:
        """Метод инициализации объекта класса парсера."""
        self.url = url
        self.user_agent = user_agent
        self.extra_data = kwargs

    # @abstractmethod
    # async def __aenter__(self) -> AsyncContextManager:
    #     """Метод инициализации для работы с асинхронным контекстным менеджером."""
    #     pass
    #
    # @abstractmethod
    # async def __aexit__(self, exc_type: type, exc_val: Exception, exc_tb: traceback) -> None:
    #     """Метод для выхода из асинхронного контекста."""
    #     pass

    @abstractmethod
    async def fetch_data(self) -> None:
        """Метод для скачивания страницы по адресу."""
        pass

    @abstractmethod
    async def parse(self) -> None:
        """Метод для извлечения данных из страницы."""
        pass

    @abstractmethod
    async def proces_data(self) -> None:
        """Метод для обработки данных например записи в БД."""
        pass


class AsyncSeleniumParser(BaseParser):
    """Класс для работы с selenium."""

    def __init__(self, url: str, user_agent: str, *args, **kwargs) -> None:
        """Инициализация объекта класса."""
        super().__init__(url, user_agent, *args, **kwargs)
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._driver = None
        self._setup_driver('chrome')

    def _setup_driver(self, driver_name: str) -> None:
        """
        Устанавливает и настраивает драйвер для работы selenium.
        :param driver_name: Имя драйвера Firefox или Chrome.
        """
        if driver_name.lower() == 'chrome':
            options = ChromeOptions()
            options.binary_location = CHROME_BINARY_LOCATION
            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-infobars')
            self._driver = webdriver.Chrome(options=options)

            stealth(driver=self._driver,
                    user_agent=self.user_agent,
                    languages=["ru-RU", "ru"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    run_on_insecure_origins=True
                    )

        elif driver_name.lower() == 'firefox':
            options = FirefoxOptions()
            options.headless = True
            # TODO заглушка для реализации firefox дравера если понадобится
            self._driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    def _fetch_data(self) -> None:
        """Функция для выполнения блокирующих операций Selenium."""
        self._driver.get(self.url)


    async def fetch_data(self) -> None:
        """Асинхронный метод для получения данных."""
        loop = asyncio.get_running_loop()
        # Выполняем блокирующую операцию в отдельном потоке
        await loop.run_in_executor(self._executor, self._fetch_data)
