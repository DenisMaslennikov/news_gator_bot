import asyncio

import fake_useragent

from app.logging import logger
from app.bot import bot, dp
from app.parsers.yandex_news import YandexNewsCategoriesParser


async def main():
    """Основная функция запускающая все процессы."""
    try:
        tasks = []
        parse = YandexNewsCategoriesParser(
            'https://dzen.ru/news',
            fake_useragent.UserAgent(browsers='chrome', platforms='pc').random,
            news_resource_id='edff6f4c-a937-48e2-8e07-cc02b1f393ac',
        )
        task = asyncio.create_task(parse.fetch_data())
        tasks.append(task)
        task = asyncio.create_task(parse.parse())
        tasks.append(task)
        task = asyncio.create_task(parse.proces_data())
        tasks.append(task)
        task = asyncio.create_task(dp.start_polling(bot))
        tasks.append(task)
        await asyncio.gather(*tasks)
    except Exception as e:
        raise e
    finally:
        await logger.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
