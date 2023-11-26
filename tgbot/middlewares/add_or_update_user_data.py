"""
    Мидлвари для работы с пользовательскими данными
"""
import logging
from pprint import pprint
from typing import Union

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.postgres.iterations.user import select_user, add_user, update_user_data
from tgbot.db.postgres.models.user import User

logger = logging.getLogger(__name__)

class UpdateUserData(BaseMiddleware):
    """
        Мидлвари которое будет срабатывать
        до того как сообщение или каллбек попадет в хендлер
    """

    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super(UpdateUserData, self).__init__()
        self.kwargs = kwargs

    async def on_pre_process_message(self, obj: types.Message, data: dict):
        """Добавляем пользователя в базу данных"""

        tg_user = obj.from_user
        user: User = await select_user(id_=tg_user.id)
        if user is None:
            await add_user(id_=tg_user.id, username=tg_user.username, fullname=tg_user.full_name)
            data["first_start"] = True

    async def on_pre_process_callback_query(self, obj: types.CallbackQuery, data: dict):
        """Добавляем пользователя в базу данных если не добавилось в предыдущий раз"""

        tg_user: types.User = obj.get("from")
        user: User = await select_user(id_=tg_user.id)
        if user is None:
            await add_user(id_=tg_user.id, username=tg_user.username, fullname=tg_user.full_name)

    async def on_post_process_message(self, 
                                      obj: Union[types.Message, types.CallbackQuery],
                                      data_from_filters: list,
                                      data: dict):
        """Обновляем данные в базе данных"""

        if type(obj) in [types.Message, types.CallbackQuery]:
            if isinstance(obj, types.CallbackQuery):
                message = obj.message
                user_id = obj.message.from_user.id
            else:
                message = obj
                user_id = obj.from_user.id

            try:
                db_user: User = await select_user(id_=user_id)

                if db_user.username != message.from_user.username:
                    await update_user_data(id_=message.from_user.id,
                                           username=message.from_user.username\
                                            if message.from_user.username is not None else "")

                if db_user.fullname != message.from_user.full_name:
                    await update_user_data(id_=message.from_user.id,
                                           fullname=message.from_user.full_name)
            except AttributeError as e:
                logger.info("Error in middlewares (UpdateUserData: on_post_process_message), error message: %s", e)
                await message.answer("Нажми /start")
