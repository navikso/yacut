import random

from settings import CHARACTERS, SHORT_AUTO_PART_LEN
from yacut.models import URLMap


def get_unique_short_id():
    characters = list(CHARACTERS)
    random.shuffle(characters)
    short_gen = "".join(
        [random.choice(characters) for x in range(SHORT_AUTO_PART_LEN)]
    )
    if URLMap.query.filter_by(short=short_gen).first() is not None:
        short_gen = get_unique_short_id()

    return short_gen


def get_validated_data(data):
    if "url" not in data:
        raise ValueError('"url" является обязательным полем!')
    if "custom_id" not in data or not data["custom_id"]:
        data["custom_id"] = get_unique_short_id()
        return data
