"""
    Описание клавиатуры для того чтобы делиться реферальной ссылкой
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def def_key_share_referal_link(link: str = "https://t.me/num04_bot") -> InlineKeyboardMarkup:
    """
        Функция возвращающая клавиатуру
    """

    key_share = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Поделиться ссылкой',
                    url=f"https://t.me/share/url?url={link}"
                ),
            ]
        ]
    )
    return key_share
