"""
    Модуль для отправки сообщений пользователям
"""
import logging
from tgbot.settings import config

logger = logging.getLogger(__name__)

async def send_message(user_id: int | str, message: str) -> dict:
    """
        Отправляем сообщение пользователю из любого места приложения
    """
    try:
        await config.bot.send_message(chat_id=user_id, text=message)
        return {"success": True}
    except Exception as e:
        logger.error("Error in sending message to user: %s", e)
        return {"success": True, "message": e}

#DISABLE