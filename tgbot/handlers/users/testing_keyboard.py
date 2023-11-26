"""
    Обработка данных с клавиатуры тестового режима
"""

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.keyboards.callback_data import for_key_binary_key
from tgbot.keyboards.inline.testing_keyboard import def_key_testing
from tgbot.misc.other.set_default_mode_data import set_default

from tgbot.states.communication import Communication


async def edit_binary_value(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """Задача состояния тестирования.  Ответ на комманду /set_testing"""
    
    key = False if callback_data.get("key") == "True" else True

    async with state.proxy() as data:
        if data.get("data_testing") is None:
            data["data_testing"] = set_default("testing")
        data["data_testing"][callback_data.get("code")] = key

    keyboard = await def_key_testing(**data["data_testing"])

    await call.message.edit_reply_markup(reply_markup=keyboard)



def register_testing_keyboard(dp: Dispatcher):
    """Регистрация хендлеров задачисостояний"""
    dp.register_callback_query_handler(edit_binary_value,
                                       for_key_binary_key.filter(code="second") | \
                                        for_key_binary_key.filter(code="searching") | \
                                            for_key_binary_key.filter(code="first"),
                                            state=Communication.testing)
