from aiogram.fsm.state import State, StatesGroup


class UnregisterConfirm(StatesGroup):
    """Состояние подтверждения удаления регистрации."""
    confirm = State()


class SubscriptionsController(StatesGroup):
    """Контролер состояний управления подписками."""
    select_subscription = State()
    update_subscription = State()
