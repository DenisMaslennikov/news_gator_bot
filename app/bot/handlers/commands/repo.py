from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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


async def get_user_repo(session: AsyncSession, user_id: int) -> User | None:
    """
    Получение пользователя по id.
    :param session:  Объект сессии SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :return: Объект модели User или None если пользователь не найден.
    """
    stmt = select(User).filter(User.user_id == user_id).options(joinedload(User.subscriptions))
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user

async def delete_all_user_subscriptions_repo(session: AsyncSession, user: User) -> None:
    """
    Удаляет все подписки пользователя.
    :param session: Объект сессии SQLAlchemy.
    :param user: Объект модели Users у которого необходимо удалить подписки.
    """
    if user.subscriptions:
        user.subscriptions.delete()


async def delete_user_repo(session: AsyncSession, user: User) -> None:
    """
    Удаляет пользователя из базы данных
    :param session: Объект сессии SQLAlchemy.
    :param user: Объект модели User который необходимо удалить.
    """
    if user:
        await session.delete(user)

