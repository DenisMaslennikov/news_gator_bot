import asyncio

from aiogram import Bot

from app.bot.functions import send_message_to_user
from app.config.constants import MESSAGE_POLING_INTERVAL
from app.db.repo import get_news_for_send_repo
from app.db.session import session_scope
from app.logging import logger
from app.queue import add_task_to_message_queue, get_task_from_message_queue


async def messages_polling_loop() -> None:
    """Цикл создание задач на отправку сообщений в бота."""
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


async def send_message_loop(bot: Bot) -> None:
    """
    Отправляет сообщения из очереди в бот.

    :param bot: Бот в которые будут отправляться сообщения.
    """
    while True:
        task = await get_task_from_message_queue()
        message = (f'<b>{task.news_title}</b>\n{task.news_date.strftime("%d.%m.%Y %H:%M")}\n{task.news_content}\n<a href="{task.news_url}">Источник</a>')
        loop = asyncio.get_running_loop()
        loop.create_task(send_message_to_user(bot, task.user_id, message))
