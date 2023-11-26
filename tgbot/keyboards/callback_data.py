"""
    Файл для обозначения данных, 
    приходящих от пользователей по inline клавиатуре
"""

from aiogram.utils.callback_data import CallbackData

for_key_back = CallbackData(
    "back", "command"
) # Пример создания калл-бэка
"""command: 'back'"""

for_key_binary_key = CallbackData(
    "binary key", "code", "key"
) # Callback для двоичных ключей (да/нет)
"""code: str / key: True or False"""

for_key_arrow_controls = CallbackData(
    "arrow controls", "direction"
) # direction (up / down)
"""direction: 'up' or 'down'"""
