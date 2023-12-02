"""
    Модуль описания получения строки даты 
"""
from datetime import datetime
from tgbot.db.postgres.iterations.subscription import select_subs

from tgbot.misc.other.localize_datetime import get_localize_by_moscow


async def get_str_end_time(own_end_time: datetime = None, user_id: int | str = None) -> str:
    """
        Возвращает время окончания подписки пользователя
    """
    if user_id is not None:
        subs = await select_subs(user_id)
        own_end_time = subs.end_time

    end_time = get_localize_by_moscow(own_end_time)

    return end_time.strftime("%d.%m.%Y (%A) в %H:%M [по МСК]")
