import asyncio

from config import settings
from app_logging import logger


async def main():
    """Основная функция запускающая все процессы."""
    try:
        # print('success')
        print(settings.base_dir)
        await logger.debug('success')
    except Exception as e:
        raise e
    finally:
        await logger.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
