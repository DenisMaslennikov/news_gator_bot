from aiogram import Router, types
from aiogram.filters import Command

from app.logging import logger

command_router = Router()


@command_router.message(Command('start', 'help'))
async def start_command_handler(message: types.Message) -> None:
    """
    Обработчик команды start и help.

    :param message: Объект сообщения от пользователя.
    """
    user_id = message.from_user.id
    await logger.debug(f'получена команда "start" от пользователя {user_id}')
    await message.answer(
        '''
Здравствуйте! Вас приветствует бот новостных подписок.
Вот список доступных команд:
/register - зарегистрироваться для получения новостей
/subscriptions - управление подписками
/get_random_news - получить случайную новость
/help - помощь
        '''
    )
