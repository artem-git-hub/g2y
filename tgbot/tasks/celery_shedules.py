"""
    Определение переодических задач для Celery
"""
from celery.schedules import crontab

celery_schedules = {

    # subscription
    'check-and-notify-subscriptions': {
        'task': 'tgbot.tasks.subscription.check_and_notify_subscriptions',
        'schedule': crontab(minute=0, hour='*'),
    }
}
