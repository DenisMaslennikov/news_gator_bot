from aiogram import Bot, Dispatcher

from config import settings

from .handlers import command_router

bot = Bot(token=settings.telegram_token)
dp = Dispatcher()

dp.include_router(command_router)

async def start_polling(dp: Dispatcher):
    """Запускает пулинг у выбранного диспетчера."""
    await dp.start_polling()
