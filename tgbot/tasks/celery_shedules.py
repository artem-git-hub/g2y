"""
    Определение переодических задач для Celery
"""
from celery.schedules import crontab

celery_schedules = {

    # subscription
    'check-and-notify-subscriptions': {
        'task': 'tgbot.tasks.subscription.check_and_notify_subscriptions',
        'schedule': crontab(minute=0, hour='*'),
    },
    'add-subscriptions-days': {
        'task': 'tgbot.tasks.subscription.add_subscriptions_days',
        'schedule': crontab(minute=0,
                            hour=0,
                            day_of_month=1,
                            month_of_year='*'),
    }
}
