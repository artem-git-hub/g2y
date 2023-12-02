"""
    Определение функций взаимодействия с базой данных для модели User
"""
import logging
from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db.postgres.db import db_query
from tgbot.db.postgres.models.user import User


logger = logging.getLogger(__name__)


@db_query
async def add_user(id_: int | str,
                   username: str = "",
                   fullname: str = "",
                   session: AsyncSession = None):
    """Добавление пользователя [id_: str | int, username: str, fullname: str]"""
    try:
        id_ = int(id_) if isinstance(id_, str) else id_
        user = User(id=id_, username=username, fullname=fullname)
        session.add(user)
        # await session.commit()
    except UniqueViolationError as e:
        logger.info("Error in created user func, message: %s", e)


@db_query
async def select_all_users(session: AsyncSession = None) -> List[User]:
    """Выборка всех созданных пользователей"""
    users = await session.execute(select(User))
    return users.fetchall()


@db_query
async def select_user(id_: int, session: AsyncSession = None) -> User:
    """Выборка конкретного пользователя по его tg id [id_: str] """
    user = (await session.execute(select(User).where(User.id == id_))).first()
    return user if user is None else user[0]


@db_query
async def count_users(session: AsyncSession = None) -> int:
    """Получение количества пользователей"""
    total = await session.scalar(select(User).count())
    return total


@db_query
async def update_user_data(id_: int,
                           username: str = "",
                           fullname: str = "",
                           session: AsyncSession = None):
    """
        Обновление данных о пользоветеле по его tg id [id_: int, username: str, fullname: str]
    """
    user = await session.get(User, id_)
    if username:
        user.username = username
    if fullname:
        user.fullname = fullname
