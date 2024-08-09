from aiogram.fsm.state import StatesGroup, State


class UnregisterConfirm(StatesGroup):
    """Состояние подтверждения удаления регистрации."""
    confirm = State()
