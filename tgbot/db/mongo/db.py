"""
    Модуль подключения к MongoDB
"""
import logging

from pymongo import MongoClient

from tgbot.settings import config
from tgbot.settings import MONGO_URI as mongo_uri

logger = logging.getLogger(__name__)


def get_db():
    """
        Подключение к MongoDB и возвращение db
    """

    try:

        logger.info("Database connection. Wait for Mongo Database...")

        client = MongoClient(mongo_uri)
        db = client[config.db.mongo.db]
        logger.info("Ready. Successful MONGO database connection.")
        return db

    except Exception as e:
        logger.error("Failed to establish connection with Mongo Database.")
        logger.info("Error in connected to Mongo: %s", e)


def get_collection(collection_name: str):
    """Функция подключения к базе данных Mongo DB"""

    try:

        db = get_db()
        return db[collection_name]

    except Exception as e:
        logger.info("Error in connection to DB: %s", e)
