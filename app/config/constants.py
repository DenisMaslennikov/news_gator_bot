import os.path

# Настройка логирования
CONSOLE_LOG_LEVEL = 'DEBUG'
FILE_LOG_LEVEL = 'WARNING'
LOG_FORMAT = '%(asctime)s | %(levelname)s | %(funcName)s | %(lineno)d | %(message)s'
LOG_FILE = os.path.join('logs', 'bot.log')