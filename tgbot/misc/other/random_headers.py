"""
    Выдача рандомных заголовков
"""

import random

from fake_useragent import UserAgent

def get_important_headers(version: str = "v2") -> list:
    """Выдача обязательных заголовков | version: str = v1/v2"""

    if version == "v1":
        accept_header_item = ["q=0.9,image/avif,image/webp,image/apng,*/*", "q=0.8,application/signed-exchange", "v=b3", "q=0.7"]
        count_headers = random.randint(0, len(accept_header_item))
        random_accept_headers = ""

        for _ in range(count_headers):
            index_ = random.randint(0, len(accept_header_item) - 1)
            random_accept_headers += ";" + accept_header_item[index_]
            accept_header_item.remove(accept_header_item[index_])

        accept_header = "text/html,application/xhtml+xml,application/xml" + random_accept_headers
    else:
        media_types = ['text/html', 'application/xhtml+xml', 'application/xml', 'image/webp', 'image/apng', '*/*']
        q_values = [f'q={random.uniform(0.5, 1):.1f}' for _ in range(len(media_types))]
        accept_header_parts = [f'{media_types[i]};{q_values[i]}' for i in range(len(media_types))]
        accept_header = ','.join(accept_header_parts)

    ua = UserAgent()

    return [
        ["Accept", accept_header],
        ["User-Agent", ua.random],
    ]

def get_random_headers() -> list:
    """Функция выдачи дополнительных рандомных заголовков"""

    list_of_headers = [
        ['Accept-Encoding', 'gzip, deflate, br'],
        ['Accept-Language', 'en-US,en;q=0.9'],
        ['Cache-Control', 'max-age=0'],
        ['Device-Memory', '8'],
        ['Downlink', '6.65'],
        ['Dpr', '1'],
        ['Ect', '4g'],
        ['Rtt', '50'],
        ['Sec-Ch-Ua',
        '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'],
        ['Sec-Ch-Ua-Arch', '"x86"'],
        ['Sec-Ch-Ua-Bitness', '"64"'],
        ['Sec-Ch-Ua-Full-Version', '"119.0.6045.105"'],
        ['Sec-Ch-Ua-Full-Version-List',
        '"Google Chrome";v="119.0.6045.105", "Chromium";v="119.0.6045.105", '
        '"Not?A_Brand";v="24.0.0.0"'],
        ['Sec-Ch-Ua-Mobile', '?0'],
        ['Sec-Ch-Ua-Model', '""'],
        ['Sec-Ch-Ua-Platform', '"Linux"'],
        ['Sec-Ch-Ua-Platform-Version', '"5.15.0"'],
        ['Sec-Ch-Ua-Wow64', '?0'],
        ['Sec-Fetch-Dest', 'document'],
        ['Sec-Fetch-Mode', 'navigate'],
        ['Sec-Fetch-Site', 'same-origin'],
        ['Sec-Fetch-User', '?1'],
        ['Upgrade-Insecure-Requests', '1'],
        ['Viewport-Width', '1030']
    ]



    count_headers = random.randint(0, len(list_of_headers))

    random_headers = []

    for _ in range(count_headers):
        index_ = random.randint(0, len(list_of_headers) - 1)
        random_headers.append(list_of_headers[index_])
        list_of_headers.remove(list_of_headers[index_])

    return random_headers

def get_headers() -> dict:
    """
        Окончательная функция выдачи всех заголовков
    """

    headers_list = get_important_headers() + get_random_headers()
    headers_dict = {}
    for i in headers_list:
        headers_dict[i[0]] = i[1]

    return headers_dict
