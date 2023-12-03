"""
    Для режима тестирования
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_arrow_controls, for_key_binary_key, for_key_back
from tgbot.misc.other.get_mark import get_mark


async def def_key_testing(
    history: bool = False,
    first: bool = True,
    second: bool = True,
    searching: bool = True,
    send_text: bool = True,
    addition_information: str = "пусто",
    count_searching: int = 5
):
    """
        Функция возвращающая клавиатуру
    """

    key_testing = InlineKeyboardMarkup(
        inline_keyboard=[
            # [
            #     InlineKeyboardButton(
            #         text='Запоминать историю ' + get_mark(history),
            #         callback_data=for_key_binary_key.new(code="history", key=True)           # потом
            #     ), # type: ignore
            # ],
            [
                InlineKeyboardButton(
                    text='Первоначальный ответ ' + get_mark(first),
                    callback_data=for_key_binary_key.new(code="first", key=first)
                ), # type: ignore
            ],
            [
                InlineKeyboardButton(
                    text='Повторный ответ ' + get_mark(second),
                    callback_data=for_key_binary_key.new(code="second", key=second)
                ), # type: ignore
            ],
            [
                InlineKeyboardButton(
                    text='Отображать поиск ' + get_mark(searching),
                    callback_data=for_key_binary_key.new(code="searching", key=searching)
                ), # type: ignore
            ],
            # [
            #     InlineKeyboardButton(
            #         text='Присылать распознаный текст ' + get_mark(send_text),
            #         callback_data=for_key_binary_key.new(code="send_text", key=True)             # потом
            #     ), # type: ignore
            # ],
            # [
            #     InlineKeyboardButton(
            #         text=f'Доп. информация для GPT ({addition_information})',
            #         callback_data=for_key_binary_key.new(code="addition_information", key=True)           # потом можно добавить, в Альфа версии этого не будет
            #     ), # type: ignore
            # ],
            # [
            #     InlineKeyboardButton(
            #         text=f'Кол-во поисковой выдачи - {count_searching}',
            #         callback_data=for_key_arrow_controls.new(direction="up")
            #     ), # type: ignore
            # ],
            # [
            #     InlineKeyboardButton(
            #         text='🔽',
            #         callback_data=for_key_arrow_controls.new(direction="down")                            # потом
            #     ), # type: ignore
            #     InlineKeyboardButton(
            #         text=f'{count_searching} / 15',
            #         callback_data=for_key_arrow_controls.new(direction="up")                            # потом
            #     ), # type: ignore
            #     InlineKeyboardButton(
            #         text='🔼',
            #         callback_data=for_key_arrow_controls.new(direction="up")
            #     ), # type: ignore
            # ]
        ]
    )
    return key_testing
