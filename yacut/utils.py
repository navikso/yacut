import random

import requests
from flask import jsonify, flash, render_template

from settings import (CHARACTERS, PERMANENT_PART, SHORT_AUTO_PART_LEN,
                      SHORT_LINK_LEN, SPECIAL_CHARS, TIMEOUT_FOR_ORIGINAL)
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


def get_validated_form(form, urlmap):
    if not urlmap.short:
        urlmap.short = get_unique_short_id()
    if any(char in SPECIAL_CHARS for char in urlmap.short):
        flash("Указано недопустимое имя для короткой ссылки")
        return render_template("index.html", form=form), 400

    if URLMap.query.filter_by(short=urlmap.short).first() is not None:
        flash("Предложенный вариант короткой ссылки уже существует.")
        return render_template("index.html", form=form), 400


def get_url_by_id_or_404(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    # if not url:
    #
    #     return jsonify({"message": "Указанный id не найден"})
    return url.original
