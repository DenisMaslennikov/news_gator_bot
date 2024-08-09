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
        keyword.add(InlineKeyboardButton(text=news_source.title, callback_data=str(news_source.id)))
    return keyword.as_markup()
