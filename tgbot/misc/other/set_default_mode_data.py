"""Обозначение простой дополнительной функции"""

def set_default(mode: str) -> dict:
    """В зависимости от типа общения передает дефолтные значения | testing, searching, question"""

    if mode == "testing":
        return {
            "history": False,
            "first": True,
            "second": True,
            "searching": True,
            "send_text": True,
            "addition_information": "пусто",
            "count_searching": 5
        }
    elif mode == "searching":
        return {}
    else:
        return {}
