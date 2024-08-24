import asyncio

import aiogram

from app.config.constants import MESSAGE_POLING_INTERVAL
from app.db.repo import get_news_for_send_repo
from app.db.session import session_scope
from app.logging import logger
from app.queue import add_task_to_message_queue


async def messages_polling_loop(bot: aiogram.Bot) -> None:
    """
    Цикл создание задач на отправку сообщений в бота.

    :param bot: Бот в которые будут отправляться сообщения.
    """
    while True:
        await asyncio.sleep(MESSAGE_POLING_INTERVAL)
        async with session_scope() as session:
            message_tasks = await get_news_for_send_repo(session)
            await logger.debug(f'Получено {len(message_tasks)} новостей для отправки')
            for task in message_tasks:
                await add_task_to_message_queue(
                    user_id=task.user_id,
                    news_id=task.news_id,
                    news_title=task.news_title,
                    news_content=task.news_content,
                    news_url=task.news_url,
                    news_date=task.news_date,
                )
