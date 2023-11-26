

async def create_prompt(messages: list = None) -> list:
    """Функция создания промпта для GPT из набора сообщений пользователя"""


    prompt = [
        {"role":"user", "content": "Отвечай обязательно на русском языке"},
        {"role":"assistant", "content": "Конечно, я буду отвечать на русском языке. Чем могу помочь?"}
    ]

    if messages is not None:
        for message in messages:
            prompt += [
                {"role":"user", "content": "эта информация пригодится впоследствии: " + message},
                {"role":"assistant", "content": "Я вас понял."}
            ]

    return prompt
