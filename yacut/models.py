import random
from datetime import datetime

import requests

from settings import CHARACTERS
from yacut import db
from yacut.errors import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        self.original = data["url"]
        self.short = data["custom_id"]

    def __repr__(self):
        return "<URLMap {}>".format(self.original)


def get_unique_short_id():
    characters = list(CHARACTERS)
    random.shuffle(characters)
    short_gen = "".join([random.choice(CHARACTERS) for x in range(6)])
    return short_gen


def check_original_url(url):
    valids = 0
    try:
        requests.get(url, timeout=5)
        valids = 1
    except:  # noqa: E722
        pass
    if valids == 1:
        return url
    raise InvalidAPIUsage("Некорректный URL.", status_code=400)


def check_short_url(short_url):
    if short_url == "" or short_url is None:
        raise InvalidAPIUsage("Нет короткой ссылки", status_code=400)
    if len(short_url) >= 16:
        raise InvalidAPIUsage(
            "Указано недопустимое имя для короткой ссылки", status_code=400
        )
    if all(char in CHARACTERS for char in str(short_url)):
        return short_url
    raise InvalidAPIUsage(
        "Указано недопустимое имя для короткой ссылки", status_code=400
    )
