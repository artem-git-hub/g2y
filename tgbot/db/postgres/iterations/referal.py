"""
    Определение функций взаимодействия с базой данных для модели Referal
"""
import logging
from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db.postgres.db import db_query
from tgbot.db.postgres.models.referal import Referal
from tgbot.misc.bot.get_int_id import get_int_id


logger = logging.getLogger(__name__)


@db_query
async def add_referal(referal_id: int | str,
                      referer_id: int | str,
                      session: AsyncSession = None):
    """Добавление реферала [referal_id: str | int, referer_id: str | int]"""
    try:
        referal_id, referer_id = get_int_id(referal_id), get_int_id(referer_id)
        referal = Referal(referal_id=referal_id, referer_id=referer_id)
        session.add(referal)
    except UniqueViolationError as e:
        logger.info("Error in created referal func, message: %s", e)


@db_query
async def select_all_referals(session: AsyncSession = None) -> List[Referal]:
    """Выборка всех созданных рефералов"""
    referals = await session.execute(select(Referal))
    return referals.fetchall()


@db_query
async def select_referals_by_referer_id(referer_id: int | str,
                                        session: AsyncSession = None
                                        ) -> Referal:
    """Выборка всех рефералов реферера [referer_id: int | str] """

    referer_id = get_int_id(referer_id)
    referals = (await session.execute(select(Referal).where(Referal.referer_id == referer_id))).fetchall()
    return referals


@db_query
async def count_referals_by_referer_id(referer_id: int | str, session: AsyncSession = None) -> int:
    """Получение количества рефералов определенного реферера"""

    total = await session.scalar(select(Referal).filter(Referal.referer_id == referer_id).count())
    return total
