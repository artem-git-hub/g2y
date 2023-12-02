"""
    Определение ответов на комманды от пользователей
"""
from datetime import timedelta
import re

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.db.postgres.iterations.referal import add_referal,\
                                                 count_referals_by_referer_id,\
                                                 select_referals_by_referer_id_and_referal_id
from tgbot.keyboards.inline.share_referal_link import def_key_share_referal_link
from tgbot.misc.bot.get_referal_link import get_referal_link
from tgbot.misc.other.add_subscription_time import add_subscription_time
from tgbot.misc.other.check_and_set_subsription import check_and_set_subscription
from tgbot.misc.other.get_str_end_time import get_str_end_time
from tgbot.misc.other.get_word_day import get_word_day
from tgbot.settings import config


async def start(message: Message, first_start: bool = None):
    """Ответ на комманду /start"""

    referer_id = message.get_args()

    referal = await select_referals_by_referer_id_and_referal_id(referer_id=referer_id, referal_id=message.from_user.id)

    if referer_id != '' and referer_id != message.from_user.id and referal is None:
        await add_referal(referal_id=message.from_user.id,
                          referer_id=referer_id)

        await add_subscription_time(user_id=referer_id, add_timedelta=timedelta(days=5))
        await add_subscription_time(user_id=message.from_user.id, add_timedelta=timedelta(days=5))

        await config.bot.send_message(
            chat_id=referer_id,
            text="У вас новый реферал! + 5 дней подписки и 1 день ежемесячно\n\n\n"\
                 "/subscription - больше данных"
            )


        await message.answer("5 день подписки в подарок за то что перешел по реферальной ссылке",
                            parse_mode="markdown")
        

    await message.answer("Привет пользователь!\n\n"\
                         f"Как мной пользоваться: [КЛИК]({config.links.main_article})",
                         parse_mode="markdown")

    if first_start:

        await add_subscription_time(user_id=message.from_user.id, add_timedelta=timedelta(weeks=1))

        await message.answer("Ты здесь первый раз, поэтому тебе подарок "\
                             "- это **7 дней подписки**, с помощью которой ты "\
                            "сможешь пользоваться абсолютно всеми командами"\
                            "о которых говорилось в "\
                            f"[инструкции]({config.links.main_article})",
                            parse_mode="markdown")


async def subscription(message: Message):
    """Ответ на комманду /subscription"""
    referal_link = await get_referal_link(user_id=message.from_user.id)

    subscription: bool = await check_and_set_subscription(user_id=message.from_user.id)

    if not subscription:
        subs_text = "У вас нет подписки"
    else:
        end_time = await get_str_end_time(user_id=message.from_user.id)
        subs_text = f"<b>Ваша подписка активна до <code>{end_time}</code></b>"

    count_of_referal = await count_referals_by_referer_id(referer_id=message.from_user.id)

    await message.answer(
        f"{subs_text}\n\n\n"\
        f"<b>Всего рефералов: {count_of_referal}</b> (это {get_word_day(count_of_referal)} "\
        "безлимитной подписки В МЕСЯЦ)\n\n"\
        f"<b>Пригласить для БЕЗЛИМИТА НАВСЕГДА: <code>{30 - count_of_referal}</code></b>\n\n\n"\
        "<b>Способы получения подписки:</b> \n\n\n1) Первый раз <b>нажать /start</b> и получить "\
        "1 неделю подписки\n\n"\
        "2) <b>Пригласить человека</b> по своей реферальной ссылке и получать 1 день в месяц"\
        " за каждого приглашенного*"\
        f"\n\n\n<b>Ваша реферальная ссылка: {referal_link}</b>"\
        "\n\n<i>* - вам будет 1-го числа каждого месяца начислятся дни "\
        "бесплатной подписки за каждого приглашенного\n\n"\
        "Пример: приглашено 5 человек и у вас с 1 по 5 число безлимитная подписка,\n\n"\
        "Другой пример: если приглашено 30 человек - у вас весь месяц подписка"\
        " - т.е. безлимитная подписка НАВСЕГДА</i>",
        reply_markup= await def_key_share_referal_link(referal_link),
        disable_web_page_preview=True)


def register_user(dp: Dispatcher):
    """Регистрация хендлеров"""

    dp.register_message_handler(start, commands=["start"], state="*", regexp=re.compile(r'^\d{8,11}$'))
    dp.register_message_handler(start, commands=["start"], state="*")

    dp.register_message_handler(subscription, commands=["subscription"], state="*")
