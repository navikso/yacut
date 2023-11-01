import random

import requests

from settings import (CHARACTERS, SHORT_AUTO_PART_LEN, SHORT_LINK_LEN,
                      TIMEOUT_FOR_ORIGINAL)
from yacut import db
from yacut.models import URLMap


def get_unique_short_id():
    characters = list(CHARACTERS)
    random.shuffle(characters)
    short_gen = "".join([random.choice(characters) for x in range(SHORT_AUTO_PART_LEN)])
    if URLMap.query.filter_by(short=short_gen).first() is not None:
        short_gen = get_unique_short_id()
    short_url = short_gen
    return short_url


def check_original_url(url):
    if not requests.get(url, timeout=TIMEOUT_FOR_ORIGINAL):
        raise ValueError("Некорректный URL.")


def check_short_url(short_url):
    print("short url", short_url)
    if len(short_url) >= SHORT_LINK_LEN:
        raise ValueError("Указано недопустимое имя для короткой ссылки")

    elif not all(char in CHARACTERS for char in str(short_url)):
        raise ValueError("Указано недопустимое имя для короткой ссылки")

    elif URLMap.query.filter_by(short=short_url).first() is not None:
        raise ValueError("Предложенный вариант короткой ссылки уже существует.")

    return short_url


def get_url_by_id_or_404(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()

    return url.original


def get_validated_data(data):
    if data is None:
        raise ValueError("Отсутствует тело запроса")

    if "url" not in data:
        raise ValueError('"url" является обязательным полем!')

    check_original_url(data["url"])

    if "custom_id" not in data or not data["custom_id"]:
        data["custom_id"] = get_unique_short_id()

    check_short_url(data["custom_id"])

    return data


def get_short_link(data):
    get_validated_data(data)
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()

    return urlmap.to_dict()
