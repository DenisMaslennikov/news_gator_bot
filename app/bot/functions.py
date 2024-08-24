import aiogram
from aiogram.enums import ParseMode

from app.logging import logger


# Функция для отправки сообщения пользователю
async def send_message_to_user(bot: aiogram.Bot, user_id: int, text: str) -> None:
    """
    Отправить сообщение пользователю.

    :param user_id: Идентификатор пользователя/чата.
    :param text: Текст сообщения.
    """
    await logger.debug(f'Отправка сообщения в чат "{user_id}"')
    await bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.HTML)
