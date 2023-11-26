"""
    Модуль с определением функций создания текста для ответа пользователю
"""

async def gen_web_message(response: dict) -> str:
    """
        Возвращает текст ответа парсинга Яндекса\n
        Принимает: response - ответ от функции парсинга
    """

    search_text = f"Ссылка на страницу поиска: [КЛИК]({response['link']})\n\n\n"
    if response["success"]:
        for item in response["elements"][:5]:

            content = item["content"]

            content = content.replace("*", "")
            item_string = f"---\n[{item['title']}]({item['link']})\n```\n{content[:650]}\n```\n\n"
            search_text += item_string
    else:
        search_text += \
        "Поиск в Яндексе ну удался, попробуйте заново. \n\n" \
        "*Или самостоятельно перейдите по ссылке на страницу поиска*"
    return search_text
