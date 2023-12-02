"""
    Дополнительный модуль к боту
"""
from tgbot.settings import config


async def get_referal_link(user_id: int | str) -> str:
    """
        Выдача реферальной ссылки по user_id 
    """

    bot = await config.bot.get_me()
    return f"https://t.me/{bot.username}?start={user_id}"
