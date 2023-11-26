"""
    Модуль с функцией сохранения файла из сообщения 
"""
import logging
from aiogram.types import Message

logger = logging.getLogger(__name__)

async def save_file(message: Message) -> str:
    """
        Функция сохранения файла из сообщения
    """

    try:

        content_type = message.content_type

        file_id = ""
        if content_type == "photo":
            file_id = message.photo[-1].file_id
        elif content_type == "document":
            file_id = message.document.file_id
        else:
            raise TypeError("Не обрабатываемый тип файла")

        file = await message.bot.get_file(file_id)

        if not any(item in file.file_path for item in ["jpg", "png"]):
            raise TypeError("Документ не является изображением")

        path = "tgbot/tmp/img/" + file_id + ".jmg"
        await file.download(destination_file=path)

        return path

    except TypeError as e:
        logger.info("Ошибка в сохранении файла: %s", e)
        return ""
