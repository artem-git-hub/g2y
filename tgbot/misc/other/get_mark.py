"""Определение дополнительной функции"""

def get_mark(value: bool) -> str:
    """Возвращает галочку на Truе и крестик на False"""

    return "✅" if value else "❌"
