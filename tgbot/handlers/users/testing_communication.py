"""
    Обработка общения в режиме тестирования
"""
import logging

from aiogram import Dispatcher
import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.misc.other.creating_prompt import create_prompt
from tgbot.misc.other.generation_message_text import gen_web_message
from tgbot.misc.other.set_default_mode_data import set_default
from tgbot.services.ai_response import ai_response
from tgbot.services.img_to_text import text_from_message
from tgbot.services.web_search import web_response

from tgbot.states.communication import Communication

logger = logging.getLogger(__name__)

async def user_start_testing_mode(message: Message, state: FSMContext):
    """Получение изображения в режиме тестирования"""

    message_text, addition_text = await text_from_message(message)
    await message.answer(
        text="```txt\n" + message_text + 
        f"\n```*Подпись к изображению (доп. инф. для запросов):* `{addition_text if addition_text != '' else '*ничего*'}`",
        parse_mode="markdown"
    )

    async with state.proxy() as data:
        if data.get("data_testing") is None:
            data["data_testing"] = set_default("testing")
        data_testing = data.get("data_testing")

    if data_testing["first"]:
        message = await message.answer("Ожидание первичного ответа от GPT ...")
        first_response = await ai_response(
            f"{message_text} \n\n\n---\n{addition_text}",
            prompt=await create_prompt()
        )
        await message.edit_text(
            f"Первичный ответ: \n\n{first_response['message']}",
            parse_mode="markdown"
        )


    if data_testing["second"] or data_testing["searching"]:
        search_message = await message.answer("Ожидание ответа от Яндекса ...")
        response = await web_response(searching_text=f"{message_text} {addition_text}")

        if data_testing["searching"]:
            search_text = await gen_web_message(response)
            await search_message.edit_text(text=search_text, parse_mode="Markdown")
        else:
            await search_message.delete()


        if data_testing["second"]:
            message = await message.answer("Ожидание вторичного ответа от GPT "
                                    "(с данными из Яндекса) ...")
            if response["success"]:


                web_prompt = await create_prompt(
                    messages=[item["content"] for item in response["elements"][:10]]
                )

                second_response = await ai_response(
                    prompt=web_prompt,
                    message=f"{message_text} \n----\n {addition_text}"
                )
                await message.edit_text(
                    text="Вторичный ответ:\n\n" + second_response["message"],
                    parse_mode="markdown"
                )
            else:
                await message.edit_text("Не удалось получить вторичный ответ")


async def unknown_type(message: Message):
    """Функция ответа если прислан не подходящий тип (не фото/документ)"""

    await message.answer(
        "Вы находитесь в режиме тестирования, в нем вы можете присылать "
        "только фотографии (*в любом виде*)",
        parse_mode="markdown"
    )


def register_testing_communication(dp: Dispatcher):
    """Регистрация хендлеров задачисостояний"""

    dp.register_message_handler(
        user_start_testing_mode,
        state=Communication.testing,
        content_types=["document", "photo"]
    )

    dp.register_message_handler(
        unknown_type,
        state=Communication.testing,
        content_types=aiogram.types.ContentTypes.ANY
    )
