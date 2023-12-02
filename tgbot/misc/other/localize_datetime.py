"""
    Модуль локализации даты и времени
"""
from datetime import datetime
import locale
import pytz


def get_localize_by_moscow(date_time: datetime) -> datetime:
    """
        Локализуем время по Москве
    """

    zone = pytz.timezone("Europe/Moscow")

    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')

    return date_time.astimezone(zone)


def get_localize_by_utc(date_time: datetime) -> datetime:
    """
        Локализуем время по Москве
    """

    zone = pytz.timezone("UTC")

    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')

    return date_time.astimezone(zone)
