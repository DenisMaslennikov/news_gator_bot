import os

# Настройка логирования
CONSOLE_LOG_LEVEL = 'DEBUG'
FILE_LOG_LEVEL = 'WARNING'
LOG_FORMAT = '%(asctime)s | %(levelname)s | %(funcName)s | %(lineno)d | %(message)s'
LOG_FILE = os.path.join('logs', 'bot.log')

CHROME_BINARY_LOCATION = '/opt/chrome/chrome-linux64/chrome'
CHROMEDRIVER_LOCATION = '/opt/chromedriver/chromedriver-linux64/chromedriver'

MAX_SELENIUM_TASKS = 5

MESSAGE_POLING_INTERVAL = 10

NEWS_ACTUAL_TIME = MESSAGE_POLING_INTERVAL * 200  # TODO Уменьшить в 100 раз
