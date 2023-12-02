"""
    Модуль с описанием проверки подлинности подписки
"""
from datetime import datetime
from tgbot.db.postgres.iterations.subscription import select_subs, update_subs_data
from tgbot.misc.bot.get_int_id import get_int_id
from tgbot.misc.other.localize_datetime import get_localize_by_utc


async def check_and_set_subscription(user_id: int | str) -> bool:
    """
        Проверка, является ли подписка пользователя действующей
    """
    user_id = get_int_id(user_id)

    db_subs = await select_subs(user_id)

    if db_subs.end_time is None:
        return False

    end_date, now_date = get_localize_by_utc(
        db_subs.end_time), get_localize_by_utc(datetime.now())

    if now_date > end_date:
        update_subs_data(user_id, end_time=None)
        return False
    return True
