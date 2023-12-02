"""
    Файл запуска двух админок
"""
import logging
import os
import subprocess
import signal
from admins.mongo.main import start_mongo_admin

from tgbot.settings import config
from tgbot.settings import POSTGRES_ADMIN_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


try:

    logger.info("Starting connected to POSTGRES admin ...")

    postgres_start_command = [
        "uvicorn",
        f"{POSTGRES_ADMIN_PATH}.main:app",
        "--host", config.admin.postgres_host,
        "--port", config.admin.postgres_port,
        "--reload"
    ]
    postgres_start = subprocess.Popen(postgres_start_command)

    logger.info("Successfull connected to POSTGRES admin!")


    logger.info("Starting connected to MONGO admin ...")


    logger.info("LINK: Mongo admin address: http://%s:%s/admin", config.admin.mongo_host, config.admin.mongo_port)
    logger.info("LINK: Postgres admin address: http://%s:%s/admin", config.admin.postgres_host, config.admin.postgres_port)

    start_mongo_admin(
        host=config.admin.mongo_host,
        port=config.admin.mongo_port
    )

    postgres_start.wait()

except KeyboardInterrupt:
    os.kill(postgres_start.pid, signal.SIGINT)
    postgres_start.wait()
