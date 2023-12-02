"""
    Модуль преобразования строчного id в числовое id
"""

def get_int_id(id_):
    """Функция преобразования id"""
    return int(id_) if isinstance(id_, str) else id_
