"""
    Файл создания конфигурационных классов и загрузки из .env файла переменных окружения 
"""
from dataclasses import dataclass
from typing import List

from aiogram import Bot
from environs import Env


@dataclass
class TgBot:
    """Класс конфигурации бота"""

    token: str
    admin_ids: List[int]
    use_redis: bool
    use_db: bool


@dataclass
class Docker:
    """Класс конфигурации докера"""

    db_container_name: str
    bot_container_name: str
    mongo_container_name: str
    redis_container_name: str


@dataclass
class Mongo:
    """Класс конфигурации MongoDB"""

    db: str
    username: str
    password: str
    host: str
    port: int

@dataclass
class Admin:
    """Класс конфигурации бота"""

    mongo_host: str
    mongo_port: str

    postgres_host: str
    postgres_port: str

@dataclass
class Redis:
    """Класс конфигурации бота"""

    host: str
    port: str


@dataclass
class ProjectLinks:
    """Класс хранения ссылок для бота"""
    main_article: str = ""
    get_maximum: str = ""


@dataclass
class Miscellaneous:
    """Класс для других параметров (опционально), не заполняется"""

    other_params: str = ""



@dataclass
class DbConfig:
    """Класс для конфигурации базы данных"""

    host: str
    password: str
    user: str
    database: str
    port: int
    debug: bool
    mongo: Mongo


@dataclass
class Config:
    """Общий класс конфигурации"""

    project_name: str
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    docker: Docker
    admin: Admin
    redis: Redis
    links: ProjectLinks
    bot: Bot



def load_config(path: str = ""):
    """
        Функция загрузки конфигурационных переменных в класс конфигурации
    """

    env = Env()
    env.read_env(path)

    return Config(
        project_name=env.str("PROJECT_NAME"),
        bot=None,
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            use_db=env.bool("USE_DB")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.int('DB_PORT'),
            debug=env.bool('DEBUG'),
            mongo=Mongo(
                db=env.str('MONGO_DB_NAME'),
                username=env.str('MONGO_USERNAME'),
                password=env.str('MONGO_PASSWORD'),
                host=env.str('MONGO_DB_HOST'),
                port=env.str('MONGO_DB_PORT')
            )
        ),
        docker=Docker(
            db_container_name=env.str('DB_CONTAINER_NAME'),
            bot_container_name=env.str('BOT_CONTAINER_NAME'),
            mongo_container_name=env.str('MONGO_DB_CONTAINER_NAME'),
            redis_container_name=env.str('REDIS_CONTAINER_NAME')
        ),
        admin=Admin(
            mongo_host=env.str('ADMIN_MONGO_HOST'),
            mongo_port=env.str('ADMIN_MONGO_PORT'),
            postgres_host=env.str('ADMIN_POSTGRES_HOST'),
            postgres_port=env.str('ADMIN_POSTGRES_PORT')
        ),
        redis=Redis(
            host=env.str('REDIS_HOST'),
            port=env.str('REDIS_PORT')
        ),
        links=ProjectLinks(),
        misc=Miscellaneous()
    )
