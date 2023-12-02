"""
    Формы для Flask админки для MongoDB
"""

from wtforms import form, fields

class UserForm(form.Form):
    """
        Модель отображения пользовател
    """
    user_id = fields.IntegerField('user_id')
    messages = fields.StringField('messages')
