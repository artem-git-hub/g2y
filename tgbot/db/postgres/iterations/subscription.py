"""
    Определение функций взаимодействия с базой данных для модели User
"""
from datetime import datetime
import logging
from typing import List, Tuple

from asyncpg import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db.postgres.db import db_query
from tgbot.db.postgres.models.subscription import Subscription
from tgbot.misc.bot.get_int_id import get_int_id


logger = logging.getLogger(__name__)


@db_query
async def add_subs(user_id: int | str,
                   end_time: datetime,
                   session: AsyncSession = None):
    """
        Добавления подписки для пользователя [user_id: str | int, end_time: datetime]
    """
    try:
        user_id = get_int_id(user_id)
        sub = Subscription(user_id=user_id, end_time=end_time)
        session.add(sub)
    except UniqueViolationError as e:
        logger.info("Error in created sub func, message: %s", e)


@db_query
async def select_all_subs(session: AsyncSession = None) -> List[Subscription]:
    """
        Выборка всех созданных подписок
    """
    subs = await session.execute(select(Subscription))
    return [i[0] for i in subs.fetchall()]


@db_query
async def select_subs(user_id: int | str,
                      session: AsyncSession = None) -> Subscription:
    """
        Выборка конкретной подписки по user_id [id_: int | str]
    """
    user_id = get_int_id(user_id)

    subs = (await session.execute(select(Subscription).where(Subscription.user_id == user_id))).first()
    return subs if subs is None else subs[0]


@db_query
async def count_subs(session: AsyncSession = None) -> int:
    """Получение количества подписок"""
    total = await session.scalar(select(Subscription).count())
    return total


@db_query
async def update_subs_data(user_id: int | str,
                           end_time: datetime,
                           session: AsyncSession = None):
    """Обновление времени окончания подписки"""

    subscription = await session.execute(
                select(Subscription).where(Subscription.user_id == user_id)
            )
    subscription: Subscription = subscription.fetchone()[0]

    if subscription:
        subscription.end_time = end_time
    else:
        return


@db_query
async def select_subs_between_time_time(first_time: datetime,
                                        second_time: datetime,
                                        session: AsyncSession = None) -> Tuple[Subscription]:
    """Выборка подписок во временом промежутке между first_time и second_time"""

    result = await session.execute(
        select(Subscription).filter(
            Subscription.end_time.between(first_time, second_time)
        )
    )
    
    return result.scalars().all()
