"""
    Определение модели реферала
"""
from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


from tgbot.db.postgres.db import TimedBaseModel
from tgbot.db.postgres.models.user import User

class Referal(TimedBaseModel):
    """
        Базовая модель реферала
    """

    __tablename__ = "referals"

    id = Column(BigInteger, autoincrement=True, primary_key=True)

    referer_id = Column(BigInteger, ForeignKey('users.id'))
    referal_id = Column(BigInteger, ForeignKey('users.id'))


    @declared_attr
    def referal(self):
        """Связь с приглашенным пользователем"""
        return relationship(User,
                            primaryjoin=User.id == self.referal_id)


    @declared_attr
    def referer(self):
        """Связь с пригласившим пользователем"""
        return relationship(User,
                            primaryjoin=User.id == self.referer_id)
