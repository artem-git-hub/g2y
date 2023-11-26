"""
    Взаимодействие с коллекцией истории общения
"""
from tgbot.misc.bot.get_int_id import get_int_id
from tgbot.db.mongo.db import get_collection

collection = get_collection("communication_history")


async def upsert_communication_history(user_id: int | str, communication_history_data: list):
    """Вставка или обновление документа в коллекции"""

    user_id = get_int_id(user_id)

    # Создание нового документа с цепочкой сообщений
    communication_history_document = {'user_id': user_id, 'messages': communication_history_data}

    collection.update_one(
        {'user_id': user_id},
        {'$set': communication_history_document},
        upsert=True
    )


async def get_communication_history(user_id: int | str):
    """Получение документа из коллекции по user_id"""
    user_id = get_int_id(user_id)

    communication_history_document = collection.find_one({'user_id': user_id})

    if communication_history_document is None:
        return None
    else:
        return communication_history_document["messages"]
