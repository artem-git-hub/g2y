"""
    Файл определения админки для PostgreSQL
"""
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import create_engine

from admins.postgres.admin_models import ReferalAdmin, SubscriptionAdmin, UserAdmin
from tgbot.settings import POSTGRES_URI

engine = create_engine(POSTGRES_URI)

app = FastAPI()
admin = Admin(app, engine=engine)

admin.add_view(UserAdmin)
admin.add_view(SubscriptionAdmin)
admin.add_view(ReferalAdmin)
