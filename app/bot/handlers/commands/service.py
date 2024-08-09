from sqlalchemy.orm import subqueryload

from app.bot.handlers.commands.repo import register_user_repo, get_user_repo, delete_all_user_subscriptions_repo, \
    delete_user_repo
from app.db.models import User
from app.db.session import session_scope


async def register_user(user_id: int) -> str:
    """
    Регистрация пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Строка со статусом регистрации.
    """
    async with session_scope() as session:
        return await register_user_repo(session, user_id)


async def delete_user(user_id: int) -> bool:
    """
    Регистрация пользователя.

    :param user_id: Идентификатор пользователя.
    :return: True если пользователь удален и False если пользователь не найден.
    """
    async with session_scope() as session:
        user = await get_user_repo(session, user_id, subqueryload(User.subscriptions))
        if user:
            await delete_all_user_subscriptions_repo(session, user)
            await delete_user_repo(session, user)
            return True
        return False

async def get_user(user_id: int) -> User | None:
    """
    Получение информации о регистрации пользователя.
    :param user_id: Идентификатор пользователя
    """
    async with session_scope() as session:
        return await get_user_repo(session, user_id)
