from app.bot.handlers.commands.repo import register_user_repo
from app.db.session import session_scope


async def register_user(user_id: int) -> str:
    """
    Регистрация пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Строка со статусом регистрации.
    """
    async with session_scope() as session:
        return await register_user_repo(session, user_id)
