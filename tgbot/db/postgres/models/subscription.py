"""
    Определение модели подписки
"""

from sqlalchemy import Column, BigInteger, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


from tgbot.db.postgres.db import TimedBaseModel
from tgbot.db.postgres.models.user import User


class Subscription(TimedBaseModel):
    """
        Базовая модель пользователя
    """

    __tablename__ = "subsriptions"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True)
    end_time = Column(DateTime(timezone=True))

    @declared_attr
    def user(self):
        """Связь с рефералом пригласившим пользователя"""
        return relationship(User,
                            primaryjoin=User.id == self.user_id)
