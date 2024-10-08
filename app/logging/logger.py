from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler

from app.config.constants import CONSOLE_LOG_LEVEL, FILE_LOG_LEVEL, LOG_FILE, LOG_FORMAT
from config import settings

formatter = Formatter(fmt=LOG_FORMAT)

# Создаем асинхронный обработчик для консольного вывода
console_handler = AsyncStreamHandler(level=CONSOLE_LOG_LEVEL, formatter=formatter)

# Создаем асинхронный обработчик для записи в файл
file_handler = AsyncFileHandler(filename=settings.base_dir / LOG_FILE, mode='a', encoding='utf-8')
file_handler.formatter = formatter
file_handler.level = FILE_LOG_LEVEL

logger = Logger(name=__name__)
logger.add_handler(console_handler)
logger.add_handler(file_handler)
