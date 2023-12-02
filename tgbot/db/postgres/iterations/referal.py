"""
    Определение функций взаимодействия с базой данных для модели Referal
"""
import logging
from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import select, func
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
async def select_referals_by_referer_id_and_referal_id(referer_id: int | str,
                                                       referal_id: int | str,
                                                       session: AsyncSession = None
                                                       ) -> Referal:
    """Выборка всех рефералов реферера [referer_id: int | str] """

    referer_id = get_int_id(referer_id)
    referal = (await session.execute(select(Referal).where(Referal.referer_id == referer_id).where(Referal.referal_id == referal_id))).fetchone()
    return referal if referal is None else referal[0]


@db_query
async def count_referals_by_referer_id(referer_id: int | str, session: AsyncSession = None) -> int:
    """Получение количества рефералов для конкретного реферера."""
    referer_id = get_int_id(referer_id)
    total = await session.scalar(
        select(func.count())
        .where(Referal.referer_id == referer_id)
    )
    return total


@db_query
async def count_referals_all_referers(session: AsyncSession = None) -> dict:
    """Получение количества рефералов для каждого реферера."""
    result = await session.execute(
        select(Referal.referer_id, func.count())
        .group_by(Referal.referer_id)
    )

    referal_counts = dict(result.fetchall())
    return referal_counts
