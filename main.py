import asyncio

from app.logging import logger
from app.bot import bot, dp
from app.tasks.parse import parse_resources_loop, parse_categories_loop, parse_queue_loop


async def main():
    """Основная функция запускающая все процессы."""
    try:
        tasks = []
        tasks.append(asyncio.create_task(parse_queue_loop()))
        tasks.append(asyncio.create_task(parse_resources_loop()))
        tasks.append(asyncio.create_task(parse_categories_loop()))
        tasks.append(asyncio.create_task(dp.start_polling(bot)))
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.exception(e)
        raise e
    finally:
        await logger.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
