"""
    Задачи связанные с подписками
"""
from datetime import datetime, timedelta
import logging
import time

from celery_module import celery_app
from tgbot.db.postgres.iterations.referal import count_referals_all_referers
from tgbot.db.postgres.iterations.subscription import select_subs_between_time_time
from tgbot.misc.other.add_subscription_time import add_subscription_time
from tgbot.misc.other.get_str_end_time import get_str_end_time
from tgbot.misc.other.localize_datetime import get_localize_by_utc
from tgbot.settings import config
from tgbot.tasks.run_async_func_in_celery import run_async

logger = logging.getLogger(__name__)

@celery_app.task
def check_and_notify_subscriptions():
    """
        Задача Celery для предупреждения пользователей о том, что заканчивается подписка
    """
    try:
        current_time = get_localize_by_utc(datetime.now())
        subscriptions_to_notify = run_async(
            select_subs_between_time_time,
            first_time=current_time + timedelta(days=1),
            second_time=current_time + timedelta(days=1, minutes=59, seconds=59)
        )

        for subscription in subscriptions_to_notify:
            end_time = run_async(get_str_end_time,
                                 own_end_time = subscription.end_time)

            run_async(config.bot.send_message,
                      chat_id=subscription.user_id,
                      text=f"Ваша подписка заканчивается {end_time}")
            time.sleep(0.5)

    except Exception as e:
        logger.exception("Error in %s: %s", __name__, e)


@celery_app.task
def add_subscriptions_days():
    """
        Задача Celery для предупреждения пользователей о том, что заканчивается подписка
    """
    try:


        referers = run_async(count_referals_all_referers)

        for referer in referers:
            run_async(add_subscription_time,
                      user_id=referer,
                      add_timedelta=timedelta(days=referers[referer]))

    except Exception as e:
        logger.exception("Error in %s: %s", __name__, e)
