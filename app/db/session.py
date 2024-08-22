import contextlib
import traceback

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.logging import logger
from config import settings

engine = create_async_engine(settings.async_database_uri)
async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

@contextlib.asynccontextmanager
async def session_scope() -> AsyncSession:
    """Создание контекстного менеджера сессии и оборачивание её в транзакцию."""
    async with async_session_factory() as sess:
        try:
            yield sess
        except OperationalError as e:
            await sess.rollback()
            raise e
        except Exception as e:
            await sess.rollback()
            logger.error(f'Необработанная ошибка: {str(e)}')
            logger.error(traceback.format_exc())
            raise e
        else:
            await sess.commit()
        finally:
            await sess.close()

