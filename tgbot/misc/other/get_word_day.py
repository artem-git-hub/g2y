"""
    Модуль который помогает со словом 'день'
"""

def get_word_day(count_day: int) -> str:
    """
        В зависимости от кол-ва дней возвращает правильное склонение слова "день"
    """
    days = ['день', 'дня', 'дней']

    if count_day % 10 == 1 and count_day % 100 != 11:
        index_ = 0
    elif 2 <= count_day % 10 <= 4 and (count_day % 100 < 10 or count_day % 100 >= 20):
        index_ = 1
    else:
        index_ = 2

    return str(count_day) + ' ' + days[index_]
