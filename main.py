import asyncio
from multiprocessing import Process

from app.bot import bot, dp
from app.logging import logger
from app.tasks.messages import messages_polling_loop, send_message_loop
from app.tasks.parse import parse_categories_loop, parse_queue_loop, parse_resources_loop


def run_polling(bot) -> None:
    """Функция для запуска polling в отдельном процессе."""
    asyncio.run(dp.run_polling(bot))


async def main():
    """Основная функция запускающая все процессы."""
    try:
        tasks = []
        # tasks.append(asyncio.create_task(dp.start_polling(bot)))
        proces = Process(target=run_polling, args=(bot,))
        proces.start()
        tasks.append(asyncio.create_task(parse_queue_loop()))
        tasks.append(asyncio.create_task(parse_resources_loop()))
        tasks.append(asyncio.create_task(parse_categories_loop()))
        tasks.append(asyncio.create_task(messages_polling_loop()))
        tasks.append(asyncio.create_task(send_message_loop(bot)))
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.exception(e)
        raise e
    finally:
        await logger.shutdown()
        proces.join()


if __name__ == '__main__':
    asyncio.run(main())
