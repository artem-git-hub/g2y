"""
    Файл для запуска MongoDB аддминки
"""
from flask import Flask
import flask_admin

from admins.mongo.views import UserView
from tgbot.db.mongo.db import get_db


def start_mongo_admin(host: str = "127.0.0.1", port: str = "5000"):
    """
        Функция запуска админки для MongoDB
    """

    db = get_db()


    app = Flask(__name__)

    app.config['MONGO_CONNECT'] = True
    app.secret_key = 'secret'


    admin = flask_admin.Admin(app, name='Mongo admin', template_mode="bootstrap4")

    # Подключаем views
    admin.add_view(UserView(db['communication_history']))

    # Запускаем
    # app.run(debug=True, host=host, port=port)
    app.run(host=host, port=port)
