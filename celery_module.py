"""
    Основной модуль для утилиты отложенных задач
"""
from celery import Celery
from tgbot.settings import config

from tgbot.settings import CELERY_BROKER_URL
from tgbot.tasks.celery_shedules import celery_schedules
    

def create_celery_app() -> Celery:
    """
        Создаем приложение Celery
    """

    app = Celery(config.project_name,
                 brocker=CELERY_BROKER_URL,
                 backend=CELERY_BROKER_URL,
                 include=["tgbot.tasks.subscription"])

    app.conf.broker_url = CELERY_BROKER_URL

    app.conf.beat_schedule = celery_schedules

    return app

celery_app = create_celery_app()
