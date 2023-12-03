"""
    Обработка общения в режиме тестирования
"""
import logging

from aiogram import Dispatcher
import aiogram
from aiogram.types import Message

from tgbot.services.img_to_text import text_from_message
from tgbot.states.communication import Communication

logger = logging.getLogger(__name__)

async def user_start_recognition_mode(message: Message):
    """Получение изображения в режиме тестирования"""

    message_text, addition_text = await text_from_message(message)
    await message.answer(
        text="```txt\n" + message_text + \
        f"\n```*Подпись к изображению:* `{addition_text if addition_text != '' else '*ничего*'}`",
        parse_mode="markdown"
    )

async def unknown_type(message: Message):
    """Функция ответа если прислан не подходящий тип (не фото/документ)"""

    await message.answer(
        "Вы находитесь в режиме распознавания, в нем вы можете присылать "
        "только фотографии (*в любом виде*)",
        parse_mode="markdown"
    )


def register_recognition_communication(dp: Dispatcher):
    """Регистрация хендлеров задачи состояний"""

    dp.register_message_handler(
        user_start_recognition_mode,
        state=Communication.recognition,
        content_types=["document", "photo"]
    )

    dp.register_message_handler(
        unknown_type,
        state=Communication.recognition,
        content_types=aiogram.types.ContentTypes.ANY
    )
