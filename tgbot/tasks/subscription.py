"""
    Задачи связанные с подписками
"""
from datetime import datetime, timedelta
import logging
import time

from celery_module import celery_app
from tgbot.misc.other.get_str_end_time import get_str_end_time
from tgbot.settings import config
from tgbot.db.postgres.iterations.subscription import select_subs_between_time_time
from tgbot.tasks.run_async_func_in_celery import run_async

logger = logging.getLogger(__name__)

@celery_app.task
def check_and_notify_subscriptions():
    """
        Задача Celery для предупреждения пользователей о том, что заканчивается подписка
    """
    try:

        current_time = datetime.utcnow()
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
