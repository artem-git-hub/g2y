import logging
from typing import List

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tgbot.config import Config

from tgbot.settings import POSTGRES_URI_ASYNC as postgres_url

logger = logging.getLogger(__name__)

Base = declarative_base()
engine = create_async_engine(postgres_url, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
)


class BaseModel(Base):
    """
    Базовая модель базы данных на которой основываются остальные.
    Здесь задается вывод каждой модели
    """
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        primary_key_columns: List[Column] = [column for column in self.__table__.columns if column.primary_key]
        values = {column.name: getattr(self, column.name) for column in primary_key_columns}
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    """
    Абстрактная модель которая содержит два столбца: время создания и последнего изменения
    """
    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )


async def wait_postgres(cfg: Config):
    """
        Функция подключения к базе данных
    """

    if cfg.db.debug:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    # connection = engine.connect()
    # version = await connection.scalar("SELECT version();")
    # await connection.close()

    # logger.info("Connected to %s", version)


async def get_session() -> AsyncSession:
    """
    Создание асинхронной сессии для подключения к БД
    """

    async with async_session() as session:
        return session

def db_query(query):
    """Декоратор передающий сессию в функции обращающиеся к базе"""

    async def wrapper(*args, **kwargs):
        try:
            async with await get_session() as session:
                result = await query(session=session, *args, **kwargs)
                await session.commit()
                await session.close_all()
                return result
        except Exception as e:
            logger.info("Error in DB func - '%s', error message: %s", query.__name__, e)
            raise

    return wrapper
