"""
    Добавляем если нет подписки в базе данных
"""
from tgbot.db.postgres.iterations.subscription import add_subs, select_subs


async def add_if_not_subscription(user_id: int | str):
    """
        Добавляем запись подписки в БД если таковая отсутствует
    """
    user_subs = await select_subs(user_id)

    if user_subs is None:
        await add_subs(user_id=user_id, end_time=None)
