from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.tools.sqlalchemy_tools import get_or_create


async def register_user_repo(session: AsyncSession, user_id: int) -> str:
    """
    Регистрация нового пользователя в базе данных.
    :param session:  Объект сессии SQLAlchemy.
    :param user_id:  Идентификатор пользователя.
    :return: Строка со статусом.
    """
    instance, created = await get_or_create(session, User, user_id=user_id)
    if created:
        return 'Вы зарегистрированы'
    return 'Вы уже зарегистрированы для управления подписками используйте меню /subscription'

