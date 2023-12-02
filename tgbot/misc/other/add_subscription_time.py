"""
    Увеличиваем время подписки
"""
from datetime import datetime, timedelta
from tgbot.db.postgres.iterations.subscription import select_subs, update_subs_data

from tgbot.misc.bot.get_int_id import get_int_id

async def add_subscription_time(user_id: int | str, add_timedelta: timedelta):
    """
        Увеличиение времени подписки для пользоваетля
    """
    user_id = get_int_id(user_id)
    user_subs = await select_subs(user_id)
    end_time = user_subs.end_time
    if end_time is None:
        end_time = datetime.now()
    end_time += add_timedelta
    await update_subs_data(user_id=user_id, end_time=end_time)
