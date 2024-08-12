from aiogram import Router, types, F
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.bot.handlers.commands.service import register_user, delete_user, get_user, subscription_status, subscribe_user, \
    unsubscribe_user, get_news_source
from app.bot.handlers.commands.stases import UnregisterConfirm, SubscriptionsController
from app.bot.handlers.keyboards.keyboards import news_source_keyboard, unsubscribe_keyboard, subscribe_keyboard
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
    if await register_user(user_id):
        await message.answer('Вы зарегистрированы')
    else:
        await message.answer('Вы уже зарегистрированы для управления подписками используйте меню /subscriptions')


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
    Обработчик подтверждения удаления регистрации.
    :param message: Объект сообщения.
    :param state: Объект состояния.
    """
    if message.text == 'yes':
        await logger.debug(f'Подтверждено удаление пользователя {message.from_user.id}')
        if await delete_user(message.from_user.id):
            await message.answer('Регистрация успешно удалена.')
        else:
            await message.answer('Пользователь не найден.')
    else:
        await logger.debug(f'Удаление пользователя {message.from_user.id} отменено')
        await message.answer('Удаление регистрации отменено.')
    await state.clear()


@command_router.message(Command('subscriptions'))
async def subscriptions_command_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды подписок.
    :param message: Объект сообщения.
    :param state: Объект состояния.
    """
    logger.debug(f'Открыто меню управления подписками для пользователя {message.from_user.id}')
    if not await get_user(message.from_user.id):
        await message.answer('Вы незарегистрированный. Зарегистрируйтесь сначала /register')
    else:
        await state.set_state(SubscriptionsController.select_subscription)
        await message.answer('Возможные ресурсы для подписки', reply_markup=await news_source_keyboard())


@command_router.callback_query(SubscriptionsController.select_subscription, F.data)
async def subscriptions_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Управление подпиской на конкретный ресурс.
    :param callback: Объект CallbackQuery.
    :param state: Объект состояния.
    """
    await logger.debug(f'Управление подпиской на {callback.data}')
    news_source_id = callback.data
    news_source = await get_news_source(news_source_id)
    response = f'Управление подпиской на {news_source.title}'
    await callback.answer(response)

    await state.update_data(news_source_id=news_source_id)

    if await subscription_status(callback.from_user.id, news_source_id):
        await callback.message.edit_text(
            response, reply_markup=unsubscribe_keyboard
        )
    else:
        await callback.message.edit_text(
            response, reply_markup=subscribe_keyboard
        )
    await state.set_state(SubscriptionsController.update_subscription)


@command_router.callback_query(SubscriptionsController.update_subscription, F.data)
async def update_subscriptions_callback_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Управление подпиской на конкретный ресурс.
    :param callback: Объект CallbackQuery.
    :param state: Объект состояния.
    """
    await logger.debug(f'Обновление статуса подписки получен статус {callback.data}')
    data = await state.get_data()
    if callback.data.lower() == 'true':
        await subscribe_user(callback.from_user.id, **data)
        await callback.answer(f'Вы подписаны')
    elif callback.data.lower() == 'back':
        pass
    elif callback.data.lower() == 'false':
        await unsubscribe_user(callback.from_user.id, **data)
        await callback.answer(f'Подписка отменена')
    await callback.message.edit_text(
        'Возможные ресурсы для подписки', reply_markup=await news_source_keyboard()
    )
    await state.set_state(SubscriptionsController.select_subscription)
