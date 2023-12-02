"""
    Определение модели пользователя
"""
from sqlalchemy import Column, BigInteger, String


from tgbot.db.postgres.db import TimedBaseModel

class User(TimedBaseModel):
    """
        Базовая модель пользователя
    """

    __tablename__ = "users"

    id = Column(BigInteger(), primary_key=True)
    username = Column(String(100), unique=True)
    fullname = Column(String)
