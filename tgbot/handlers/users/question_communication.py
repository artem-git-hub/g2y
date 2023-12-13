"""
    Обработка общения в режиме тестирования
"""
import logging

import aiogram
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.db.mongo.collections.communication_history import get_communication_history, upsert_communication_history
from tgbot.services.ai_response import ai_response
from tgbot.states.communication import Communication


logger = logging.getLogger(__name__)


async def user_start_question_mode(message: Message, state: FSMContext):
    """Получение изображения в режиме тестирования"""

    try:
        text = message.text
        user_id = message.from_user.id

        communication_history = await get_communication_history(user_id=user_id)

        message = await message.answer("Ожидание ответа от GPT ...")
        response = await ai_response(
            text,
            prompt=communication_history,
            no_16k=True
        )

        await upsert_communication_history(user_id=user_id,
                                       communication_history_data=response.get("prompt"))

        await message.edit_text(
            response['message'],
            parse_mode="markdown"
        )

    except Exception as e:
        logger.info("Error in question mode: %s", e)

async def unknown_type(message: Message):
    """Функция ответа если прислан не подходящий тип (что угодно кроме текста)"""

    await message.answer(
        "Вы находитесь в режиме ответов на вопросы, в нем вы можете присылать "
        "только *только текст*",
        parse_mode="markdown"
    )


def register_question_communication(dp: Dispatcher):
    """Регистрация хендлеров задачи состояний"""

    dp.register_message_handler(
        user_start_question_mode,
        state=Communication.question,
        content_types=["text"]
    )

    dp.register_message_handler(
        unknown_type,
        state=Communication.question,
        content_types=aiogram.types.ContentTypes.ANY
    )
