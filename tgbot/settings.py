"""
    Модуль с описанием путей или не конфиденциальных данных
"""

from tgbot.config import load_config


ENV_PATH = ".env"
"Путь к .env файлу относительно корня"

POSTGRES_ADMIN_PATH = "admins.postgres"
MONGO_ADMIN_PATH = "admins/mongo"

config = load_config(ENV_PATH)
"Подгружаем конфиг"

POSTGRES_URI_ASYNC = f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"
POSTGRES_URI = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"

MONGO_URI = f"mongodb://{config.db.mongo.username}:{config.db.mongo.password}@{config.db.mongo.host}:{config.db.mongo.port}/{config.db.mongo.db}?authSource=admin"
