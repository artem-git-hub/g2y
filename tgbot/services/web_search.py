"""
    Определение функции парсинга поиска
"""

import asyncio
import logging
import urllib.parse
import random
import requests

from bs4 import BeautifulSoup

from tgbot.misc.other.random_headers import get_headers


logger = logging.getLogger(__name__)


def request_web(request_message: str) -> dict:
    """
        Отправка запроса и получение ответа от поисковой выдачи яндекса
    """

    # request_message = request_message[:200].replace('\n', ' ')
    request_message = urllib.parse.quote(request_message)
    url = f"https://ya.ru/search/?text={request_message}&lr=39&search_source=yaru_desktop_common&search_domain=yaru"

    session = requests.Session()
    session.cookies.clear()
    session.headers.update(get_headers())


    response = session.get(url)

    answer = {"success": None, "elements": [], "message": "Ok!", "link": url}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')


        search_results = soup.find_all(class_ = "serp-item")

        results = []


        best_answer = soup.find(class_ = "SerpItem")
        if best_answer is not None:
            title = best_answer.find(class_ = "Article").text
            content = best_answer.find(class_ = "Fold-Body").text
            link = best_answer.find(class_ = "Link").get("href")

            if all((title, content, link)):
                results.append({
                    'title': str(title).replace("\n", ""),
                    'link': str(link).replace("\n", ""),
                    'content': str(content).replace("\n", "").replace(">", "")
                })

        for result in search_results:

            title_elem = result.find('h2', class_='OrganicTitle-LinkText')
            title = title_elem.text if title_elem else None


            link_elem = result.find('a', class_='OrganicTitle-Link')
            link = link_elem['href'] if link_elem else None


            content_short = result.find('span', class_='ExtendedText-Short')
            content_full = result.find('span', class_='ExtendedText-Full')
            content_elem = result.find('span', class_='OrganicTextContentSpan')
            
            content = content_full.text if content_full else None
            if content is None:
                content = content_short.text if content_short else None

            if content is None:
                content = content_elem.text if content_elem else None


            if all(bool(item) for item in [title, link, content]):
                results.append({
                    'title': str(title).replace("\n", ""),
                    'link': str(link).replace("\n", ""),
                    'content': str(content).replace("\n", "").replace(">", "")
                })

        if len(results) != 0 and response.text.count("CheckboxCaptcha-Button") == 0:
            answer["success"] = True
            answer["elements"] = results
        else:
            answer["success"] = False
            answer["message"] = "Запрос не удался. Ошибка парсинга. Вылезла капча"
    else:
        answer["success"] = False
        answer["message"] = "Запрос не удался. Статус != 200."

    logger.info(answer["message"])
    return answer


async def web_response(searching_text: str) -> dict:
    """
        Функция гарантированного запроса к поиску
    """

    response = request_web(request_message=searching_text)
    for _ in range(5):
        if response["success"]:
            break
        else:
            await asyncio.sleep(random.randint(1, 6))
            response = request_web(request_message=searching_text)

    return response
