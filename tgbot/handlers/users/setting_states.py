"""
    Обработка задания состояний общения
"""

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tgbot.keyboards.inline.testing_keyboard import def_key_testing
from tgbot.misc.other.set_default_mode_data import set_default

from tgbot.states.communication import Communication


async def set_testing(message: Message, state: FSMContext):
    """Задача состояния тестирования.  Ответ на комманду /t"""
    await Communication.testing.set()

    async with state.proxy() as data:
        if data.get("data_testing") is None:
            data["data_testing"] = set_default("testing")
        data_testing = data.get("data_testing")

    keyboard = await def_key_testing(**data_testing)

    await message.answer(
        "Вы задали состояние тестирования\n\n"
        "**Вы можете присылать фотографии "
        "(в сжатом формате [для отсутствия потери качества])**",
        reply_markup=keyboard,
        parse_mode="markdown"
    )


async def set_recognition(message: Message):
    """Задача состояния тестирования.  Ответ на комманду /r"""
    await Communication.recognition.set()
    await message.answer(
        "Вы задали состояние распознования текста с изображения\n\n"
        "Отправляйте фотографии и бот выдаст вам распознаный текст"
    )


async def set_question(message: Message):
    """Задача состояния тестирования.  Ответ на комманду /q"""
    await Communication.question.set()
    await message.answer(
        "Вы задали состояние общения c GPT\n\n"
        "Присылайте запрос и вам ответит AI по данному вопросу"
    )


async def no_subscription(message: Message, state: FSMContext):
    """
        Ответ на комманды: /q и /t без подписки
    """
    await state.reset_state()
    await message.answer(
        "У вас нет подписки, введите комманду /sub, "\
        "для получения большей информации"
    )


def register_setting_states(dp: Dispatcher):
    """Регистрация хендлеров задачисостояний"""
    dp.register_message_handler(set_testing,
                                commands=["t"],
                                state="*",
                                is_subscriber=True)
    dp.register_message_handler(set_recognition, commands=["r"], state="*")
    dp.register_message_handler(set_question,
                                commands=["q"],
                                state="*",
                                is_subscriber=True)

    dp.register_message_handler(no_subscription,
                                commands=["q", "t"],
                                state="*")
