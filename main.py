import asyncio

from app.logging import logger
from app.bot import bot, dp


async def main():
    """Основная функция запускающая все процессы."""
    try:
        task = asyncio.create_task(dp.start_polling(bot))
        await asyncio.gather(task)
    except Exception as e:
        raise e
    finally:
        await logger.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
