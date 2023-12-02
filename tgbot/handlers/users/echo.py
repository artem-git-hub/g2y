"""
    Определение функций отвечающих пользователям эхом
"""
from aiogram import types, Dispatcher


async def bot_echo_all(message: types.Message):
    """Пример эхо на любое сообщение с любым состоянием"""

    await message.answer('Скорее всего вы нажали что-то не то введите /start,' \
                         ' если это не поможет, то напишите в тех. поддержку')


def register_echo(dp: Dispatcher):
    """Регистрация всех хендлеров и прикрипление их к функциям"""

    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
