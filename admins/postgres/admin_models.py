"""
    Отображения в админке моделей
"""
from sqladmin import ModelView

from tgbot.db.postgres.models.user import User
from tgbot.db.postgres.models.subscription import Subscription

class UserAdmin(ModelView, model=User):
    """Отображение модели User"""

    column_list = [User.id, User.fullname, User.username]



class SubscriptionAdmin(ModelView, model=Subscription):
    """Отображение модели Subscription"""

    column_list = [Subscription.user_id, Subscription.end_time]
