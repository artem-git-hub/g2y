"""
    Модуль для выполнения ассинхронных функций для Celery
"""
import asyncio


loop = asyncio.get_event_loop()

def run_async(func, *args, **kwargs):
    """
        Функция в которую передаем ассинхронную функцию для ее выполнения
    """

    return loop.run_until_complete(func(*args, **kwargs))
