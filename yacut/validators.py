import requests

from settings import CHARACTERS, SHORT_LINK_LEN, TIMEOUT_FOR_ORIGINAL
from yacut.utils import get_unique_short_id
from yacut.models import URLMap


def check_original_url(data):
    if "url" not in data:
        raise ValueError('"url" является обязательным полем!')
    if not requests.get(data['url'], timeout=TIMEOUT_FOR_ORIGINAL):
        raise ValueError("Некорректный URL.")


def check_short_url(data):
    if "custom_id" not in data or not data["custom_id"]:
        data["custom_id"] = get_unique_short_id()
        return data
    custom_id = data["custom_id"]
    if len(custom_id) >= SHORT_LINK_LEN:
        raise ValueError("Указано недопустимое имя для короткой ссылки")

    elif not all(char in CHARACTERS for char in str(custom_id)):
        raise ValueError("Указано недопустимое имя для короткой ссылки")

    elif URLMap.query.filter_by(short=custom_id).first() is not None:
        raise ValueError("Предложенный вариант короткой ссылки уже существует.")

    return custom_id


def data_validator(data):
    if data is None:
        raise ValueError("Отсутствует тело запроса")

    check_original_url(data)
    check_short_url(data)
