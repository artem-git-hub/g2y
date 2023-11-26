"""
    Определение ответов на комманды от пользователей
"""

from datetime import datetime, timedelta
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.db.postgres.iterations.subscription import add_subs

async def user_start(message: Message, first_start: bool = None):
    """Ответ на комманду /start"""

    await message.answer("Привет пользователь!\n\n"\
                         "Как мной пользоваться: [КЛИК](https://telegra.ph/rpups-bot-11-26)",
                         parse_mode="markdown")

    if first_start:
        end_time = datetime.now() + timedelta(weeks=1)
        await add_subs(user_id=message.from_user.id, end_time=end_time)

        await message.answer("Ты здесь первый раз, поэтому тебе подарок "\
                             "- это **7 дней подписки**, с помощью которой ты "\
                            "сможешь пользоваться абсолютно всеми командами"\
                            "о которых говорилось в "\
                            "[инструкции](https://telegra.ph/rpups-bot-11-26)",
                            parse_mode="markdown")
        



def register_user(dp: Dispatcher):
    """Регистрация хендлеров"""

    dp.register_message_handler(user_start, commands=["start"], state="*")
