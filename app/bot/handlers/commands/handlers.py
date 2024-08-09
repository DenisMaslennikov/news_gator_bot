from aiogram import Router, types, F
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.bot.handlers.commands.service import register_user, delete_user
from app.bot.handlers.commands.stases import UnregisterConfirm
from app.logging import logger

command_router = Router()


@command_router.message(Command('start', 'help'))
async def start_command_handler(message: types.Message) -> None:
    """
    Обработчик команды start и help.

    :param message: Объект сообщения.
    """
    user_id = message.from_user.id
    await logger.debug(f'получена команда "start" от пользователя {user_id}')
    await message.answer(
        '''
Здравствуйте! Вас приветствует бот новостных подписок.
Вот список доступных команд:
/register - зарегистрироваться для получения новостей
/unregister - удалить регистрацию и все подписки
/subscriptions - управление подписками
/get_random_news - получить случайную новость
/help - помощь
        '''
    )


@command_router.message(Command('register'))
async def register_command_handler(message: types.Message) -> None:
    """
    Обработчик команды register.

    :param message:  Объект сообщения.
    """
    user_id = message.from_user.id
    await logger.debug(f'получена команда register от пользователя {user_id}')
    await message.answer(await register_user(user_id))


@command_router.message(Command('unregister'))
async def unregister_command_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды register.

    :param message: Объект сообщения.
    :param state: Объект состояния.
    """
    await logger.debug(f'Получена команда unregister от пользователя {message.from_user.id}')
    await state.set_state(UnregisterConfirm.confirm)
    await message.answer('Подтвердите действие отправив сообщение yes или отмените отправив no')


@command_router.message(UnregisterConfirm.confirm, F.text.in_(['yes', 'no']))
async def unregister_confirm(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик подтверждения удаления регистрации
    :param message: Объект сообщения.
    :param state: Объект состояния.
    """
    if message.text == 'yes':
        await logger.debug('Подтверждено удаление')
        if await delete_user(message.from_user.id):
            await message.answer('Регистрация успешно удалена.')
        else:
            await message.answer('Пользователь не найден.')
    else:
        await logger.debug('Удаление отменено')
        await message.answer('Удаление регистрации отменено.')
    await state.clear()

