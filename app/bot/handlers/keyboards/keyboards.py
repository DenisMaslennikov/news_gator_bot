from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.keyboards.service import get_news_sources, get_categories_for_resources
from app.logging import logger


async def news_source_keyboard() -> InlineKeyboardMarkup:
    """
    Получает из базы список ресурсов доступных для подписки.

    :return: Инлайн клавиатуру с вариантами подписок.
    """
    await logger.debug('Генерация клавиатуры подписок - сайты')
    keyboard = InlineKeyboardBuilder()
    news_sources = await get_news_sources()
    for news_source in news_sources:
        keyboard.add(
            InlineKeyboardButton(text=news_source.title, callback_data=str(news_source.id))
        )
    return keyboard.adjust(2).as_markup()


async def news_category_keyboard(resource_id) -> InlineKeyboardMarkup:
    """
    Получает из базы варианты подписок и создает клавиатуру с вариантами подписок.

    :return: Инлайн клавиатуру с вариантами подписок.
    """
    await logger.debug('Генерация клавиатуры подписок - категории')
    keyboard = InlineKeyboardBuilder()
    categories = await get_categories_for_resources(resource_id)
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(text=category.name, callback_data=str(category.id))
        )
    return keyboard.adjust(2).as_markup()


# Клавиатура отписки
unsubscribe_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Отписаться', callback_data='false'),
        InlineKeyboardButton(text='Назад', callback_data='back'),
    ],
])

# Клавиатура подписки
subscribe_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Подписаться', callback_data='true'),
        InlineKeyboardButton(text='Назад', callback_data='back'),
    ],
])
