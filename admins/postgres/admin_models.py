"""
    Отображения в админке моделей
"""
from sqladmin import ModelView

from tgbot.db.postgres.models.user import User
from tgbot.db.postgres.models.subscription import Subscription
from tgbot.db.postgres.models.referal import Referal


class UserAdmin(ModelView, model=User):
    """Отображение модели User"""

    column_list = [User.id, User.fullname, User.username]

    form_include_pk = True


class SubscriptionAdmin(ModelView, model=Subscription):
    """Отображение модели Subscription"""

    column_list = [Subscription.user, Subscription.end_time]


class ReferalAdmin(ModelView, model=Referal):
    """Отображение модели Subscription"""

    column_list = [Referal.referer, Referal.referal]
