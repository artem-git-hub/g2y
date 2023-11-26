
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine


engine = create_engine("postgresql://rpups_bot:rpups123_bot@127.0.0.1:5544/rpups_db")











from tgbot.db.postgres.models.user import User

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.fullname, User.username]


admin.add_view(UserAdmin)
