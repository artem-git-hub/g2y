"""
    Модуль с описанием путей или не конфиденциальных данных
"""
from aiogram import Bot
from tgbot.config import load_config


ENV_PATH = ".env"
"Путь к .env файлу относительно корня"

POSTGRES_ADMIN_PATH = "admins.postgres"
MONGO_ADMIN_PATH = "admins/mongo"

config = load_config(ENV_PATH)
"Подгружаем конфиг"

config.bot=Bot(token=config.tg_bot.token, parse_mode='HTML')

config.links.main_article = 'https://telegra.ph/g2y---GPTsearchingrecognize-12-03'
config.links.get_maximum = 'https://telegra.ph/Kak-poluchit-maksimum-ot-g2y-bot-12-03'

POSTGRES_URI_ASYNC = f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"
POSTGRES_URI = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"

MONGO_URI = f"mongodb://{config.db.mongo.username}:{config.db.mongo.password}@{config.db.mongo.host}:{config.db.mongo.port}/{config.db.mongo.db}?authSource=admin"

CELERY_BROKER_URL = f'redis://{config.redis.host}:{config.redis.port}/0'
# CELERY_BROKER_URL = f'redis://{config.docker.redis_container_name}:{config.redis.port}/0'

