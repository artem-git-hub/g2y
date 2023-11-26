from flask_admin.contrib.pymongo import ModelView

from admins.mongo.forms import UserForm

class UserView(ModelView):
    """
        Отображение колонок и присоединение шаблонов
    """

    column_list = ('user_id', 'messages')
    form = UserForm

    # edit_template = 'ch_edit_view.html'
