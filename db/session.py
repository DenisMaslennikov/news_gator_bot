import traceback

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from app_logging import logger
from config import settings

async def session_scope() -> Session:
    """Создание контекстного менеджера сессии и оборачивание её в транзакцию."""
    sess = None
    try:
        engine = create_async_engine(settings.database_uri)
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
        logger.error(f'Необработанная ошибка: {str(e)}')
        logger.error(traceback.format_exc())
        raise e
    else:
        await sess.commit()



