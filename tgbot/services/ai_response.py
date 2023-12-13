"""
    Определение функции взаимодействия с AI
"""
import logging
from re import L
from typing import Dict, Optional, Union
import g4f

logger = logging.getLogger(__name__)

async def request_gpt(
        message: str = "",
        prompt: list = None,
        no_16k: bool = False
) -> Dict[str, bool | str]:
    """
        Ассинхронный вызов разных представителей AI
        Получает: message: str - текст запроса
        Отдает: {
            "success": bool - True если запрос выполнился удачно
            "message": str - ответ от AI
        }
    """

    try:

        if prompt is None:
            prompt = []

        messages = prompt + [{"role": "user", "content": message}]

        # response = await g4f.ChatCompletion.create_async(
        #     model=g4f.models.gpt_35_turbo_16k,
        #     messages=messages,
        # )

        # logger.info("Starting AI response ...")
        # logger.info("Message: %s", message)

        if not no_16k:
            response = await g4f.ChatCompletion.create_async(
                # model=g4f.models.gpt_35_turbo,
                # model="gpt-3.5-turbo",
                model="gpt-3.5-turbo-16k",
                messages=messages,
            )
        else:
            response = await g4f.ChatCompletion.create_async(
                # model=g4f.models.gpt_35_turbo,
                model="gpt-3.5-turbo",
                #model="gpt-3.5-turbo-16k",
                messages=messages,
            )
        # response = await g4f.ChatCompletion.create_async(
        #     model=g4f.models.gpt_35_long,
        #     messages=messages,
        # )


        # response = await g4f.ChatCompletion.create_async(
        #     model=g4f.models.gpt_35_turbo_16k,
        #     messages=messages,
        # )

        # response = await g4f.ChatCompletion.create_async(
        #     model=g4f.models.gpt_4,
        #     messages=messages,
        # )
        messages.append({"role": "assistant", "content": response})

        # logger.info("Get AI response ...")
        # logger.info("Response: %s", response)

        return {"success": True, "message": str(response), "prompt": messages}
    except RuntimeError:
        logger.info("AI error RuntimeError")
        return {
            "success": False,
            "message": "Запрос к AI не удался, попробуйте заново!", "prompt": None
        }


async def ai_response(*args, **kwargs) -> Dict[str, Optional[Union[str, bool, None]]]:
    """
        Функция гарантированного ответа от GPT\n\n
        Будет запрашивать ответ 
        до тех пор пока не будет дан ответ\n
        Принимает: message: str and(or) prompt: dict 
    """

    response = await request_gpt(*args, **kwargs)

    stop_list = ["support@chatbase.co", "您的免费额度不够使用这个模型啦"]

    while not response["success"] or any([item in response["message"] for item in stop_list]) or response["message"] == "":
        response = await request_gpt(*args, **kwargs)

    return response
