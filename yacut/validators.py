import requests

from settings import CHARACTERS, SHORT_LINK_LEN, TIMEOUT_FOR_ORIGINAL
from yacut.utils import get_validated_data
from yacut.models import URLMap


def check_original_url(url):
    if not requests.get(url, timeout=TIMEOUT_FOR_ORIGINAL):
        raise ValueError("Некорректный URL.")


def check_short_url(custom_id):
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
    get_validated_data(data)
    check_original_url(data["url"])
    check_short_url(data["custom_id"])
