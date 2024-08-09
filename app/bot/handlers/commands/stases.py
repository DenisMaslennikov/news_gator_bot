from aiogram.fsm.state import StatesGroup, State


class UnregisterConfirm(StatesGroup):
    """Состояние подтверждения удаления регистрации."""
    confirm = State()

class SubscriptionsController(StatesGroup):
    """Контролер состояний управления подписками."""
    select_subscription = State()
    update_subscription = State()
