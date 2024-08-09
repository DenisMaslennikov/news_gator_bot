import contextlib
import traceback

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session

from app.logging import logger
from config import settings


@contextlib.contextmanager
async def session_scope() -> Session:
    """Создание контекстного менеджера сессии и оборачивание её в транзакцию."""
    sess = None
    conn = None
    try:
        engine = create_async_engine(settings.async_database_uri)
        conn = engine.connect()
        session = async_sessionmaker(bind=conn)
        sess = session()
        yield sess
    except OperationalError as e:
        if sess is not None:
            # Откатываем транзакцию.
            await sess.rollback()
        raise e
    except Exception as e:
        if sess is not None:
            # Откатываем транзакцию.
            await sess.rollback()
        await logger.error(f'Необработанная ошибка: {str(e)}')
        await logger.error(traceback.format_exc())
        raise e
    else:
        await sess.commit()
    finally:
        if conn is not None:
            # Закрытие соединения.
            await conn.close()
        if sess is not None:
            # Закрытие сессии.
            await sess.close()
            # Очистка сессии.
            await sess.invalidate()
