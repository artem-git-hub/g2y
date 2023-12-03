"""
    Фильтр который будет проверять наличие подписки
"""
from typing import Optional

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from tgbot.db.postgres.iterations.subscription import select_subs
from tgbot.misc.other.check_and_set_subsription import check_and_set_subscription


class SubscriptionFilter(BoundFilter):
    """
        Класс фильтра
    """

    key = 'is_subscriber'

    def __init__(self, is_subscriber: Optional[bool] = None):
        self.is_subscriber = is_subscriber

    async def check(self, obj) -> bool:
        """Метод фильтра который и выполняет главную роль"""

        user_id: Optional[Message | CallbackQuery] = obj.from_user.id

        if self.is_subscriber is None:
            return False
        if select_subs(user_id=user_id) is None:
            return False

        return await check_and_set_subscription(user_id)
