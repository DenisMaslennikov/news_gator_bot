import contextlib
import traceback

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.logging import logger
from config import settings

async_engine = create_async_engine(settings.async_database_uri)
async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)

engine = create_engine(settings.database_uri)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)


@contextlib.asynccontextmanager
async def async_session_scope() -> AsyncSession:
    """Создание контекстного менеджера асинхронных сессии и оборачивание её в транзакцию."""
    async with async_session_factory() as sess:
        try:
            yield sess
        except OperationalError as e:
            await sess.rollback()
            raise e
        except Exception as e:
            await sess.rollback()
            await logger.error(f'Необработанная ошибка: {str(e)}')
            await logger.error(traceback.format_exc())
            raise e
        else:
            await sess.commit()
        finally:
            await sess.close()


@contextlib.contextmanager
def session_scope() -> Session:
    """Создание контекстного менеджера сессии и оборачивание её в транзакцию."""
    with session_factory() as sess:
        try:
            yield sess
        except OperationalError as e:
            sess.rollback()
            raise e
        except Exception as e:
            sess.rollback()
            logger.error(f'Необработанная ошибка: {str(e)}')
            logger.error(traceback.format_exc())
            raise e
        else:
            sess.commit()
        finally:
            sess.close()
