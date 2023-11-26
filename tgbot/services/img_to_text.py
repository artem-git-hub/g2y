"""
    Распознование текста с изображения
"""
import os

from aiogram.types import Message
import pytesseract
from PIL import Image

from tgbot.misc.other.save_file import save_file


async def image_to_string(image_path: str = "") -> str:
    """
        Функция возвращающая распознаный текст 
        изображения получая на вход путь к изображению
    """

    img = Image.open(image_path)

    text = pytesseract.image_to_string(img, lang='eng+rus')

    return text


async def text_from_message(message: Message) -> set:
    """
        Вытаскивает весь текст с изображения в 
        сообщении и из описания изображения
    """

    image_path = await save_file(message)

    if not image_path:
        await message.answer("Отправьте повторно. Отправленный файл не является изображением.")

    text = await image_to_string(image_path=image_path)

    addition_text = message.caption
    if addition_text is None:
        addition_text = ""

    os.remove(image_path)

    return text, addition_text
