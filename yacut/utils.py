import random

import requests

from settings import (
    CHARACTERS,
    PERMANENT_PART,
    SHORT_AUTO_PART_LEN,
    SHORT_LINK_LEN,
    TIMEOUT_FOR_ORIGINAL,
)
from yacut.errors import InvalidAPIUsage
from yacut.models import URLMap


def get_unique_short_id():
    characters = list(CHARACTERS)
    random.shuffle(characters)
    short_gen = "".join([random.choice(CHARACTERS) for x in range(SHORT_AUTO_PART_LEN)])
    if URLMap.query.filter_by(short=short_gen).first() is not None:
        short_gen = get_unique_short_id()
    return short_gen


def check_original_url(url):
    if not requests.get(url, timeout=TIMEOUT_FOR_ORIGINAL):
        raise InvalidAPIUsage("Некорректный URL.", status_code=400)


def add_perm_in_short(short):
    if short.startswith(PERMANENT_PART):
        return short
    short_link = PERMANENT_PART + short
    return short_link


def check_short_url(short_url):
    if short_url == "" or short_url is None:
        raise InvalidAPIUsage("Нет короткой ссылки", status_code=400)
    if len(short_url) >= SHORT_LINK_LEN:
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки", status_code=400
        )
    if not all(char in CHARACTERS for char in str(short_url)):
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки", status_code=400
        )
    if URLMap.query.filter_by(short=short_url).first() is not None:
        raise InvalidAPIUsage(
            "Предложенный вариант короткой ссылки уже существует.", status_code=400
        )


def get_validated_data(data):
    if data is None:
        raise InvalidAPIUsage("Отсутствует тело запроса", status_code=400)

    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', status_code=400)

    check_original_url(data["url"])

    if "custom_id" not in data or not data["custom_id"]:
        data["custom_id"] = get_unique_short_id()

    check_short_url(data["custom_id"])
