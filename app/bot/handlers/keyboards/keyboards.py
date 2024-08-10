from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.handlers.keyboards.service import get_news_sources
from app.logging import logger


async def news_source_keyboard() -> InlineKeyboardMarkup:
    """
    Получает из базы варианты подписок и создает клавиатуру с вариантами подписок.
    :return: Инлайн клавиатуру с вариантами подписок.
    """
    await logger.debug('Генерация клавиатуры подписок')
    keyword = InlineKeyboardBuilder()
    news_sources = await get_news_sources()
    for news_source in news_sources:
        keyword.add(
            InlineKeyboardButton(text=news_source.title, callback_data=str(news_source.id))
        )
    return keyword.adjust(2).as_markup()


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
