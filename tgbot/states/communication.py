"""
    Определение вариантов общения бота
"""
from aiogram.dispatcher.filters.state import StatesGroup, State

class Communication(StatesGroup):
    """
        Типы общения:
        1) testing - общение с ответом сначала от AI, 
        после чего гуглится, выдается ответ браузера и заключение AI
        2) searching - просто идет поиск, после чего выдается ответ браузера
        3) question - ответ на вопрос AI
    """

    testing = State()
    recognition = State()
    question = State()
    