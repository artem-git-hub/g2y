"""
    Главный файл для запуска бота
"""
import asyncio
import logging

import tenacity
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.db.postgres.db import wait_postgres
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin.command import register_admin
from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.command import register_user
from tgbot.handlers.users.question_communication import register_question_communication
from tgbot.handlers.users.setting_states import register_setting_states
from tgbot.handlers.users.testing_communication import register_testing_communication
from tgbot.handlers.users.testing_keyboard import register_testing_keyboard
from tgbot.middlewares.add_or_update_user_data import UpdateUserData
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.bot.set_bot_commands import set_default_commands
from tgbot.settings import config

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    """
        Функция для регистрации всех Middleware. 
        Импортировать, после чего подключить по примеру, передав конфиг
    """
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(UpdateUserData())


def register_all_filters(dp: Dispatcher):
    """
        Регистрация всех фильтров по примеру
    """
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    """
        Регистрация всех хендреров сообщений
    """
    register_admin(dp)
    register_user(dp)

    register_setting_states(dp)

    register_testing_keyboard(dp)
    register_testing_communication(dp)

    register_question_communication(dp)

    register_echo(dp)


async def connection_db():
    """
        Функция контроля подключения к базе данных
    """
    logger.info("Database connection. Wait for Postgres Database...")
    try:
        await wait_postgres(cfg=config)
    except tenacity.RetryError:
        logger.error("Failed to establish connection with Postgres Database.")
        exit(1)
    logger.info("Ready. Successful POSTGRES database connection.")


async def main():
    """
        Главная функция по запуску бота
    """

    # Делаем настройку вывода логирования
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")



    #Используем Redis если это необходимо
    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    #Засовываем конфиг в переменную бота
    bot['config'] = config

    #Если используется БД то идет подключение к ней
    if config.tg_bot.use_db:
        await connection_db()

    #Регистрация элементов
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    #Установление всех базовых комманд
    await set_default_commands(dp)

    #Оповещение всех админов
    for admin_id in config.tg_bot.admin_ids:
        await dp.bot.send_message(admin_id, "Бот запущен!")

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close() # type: ignore

        dp.stop_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        logger.error("Bot stopped!")
