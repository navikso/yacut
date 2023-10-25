from flask import flash, jsonify, redirect, render_template, request, url_for

from settings import PERMANENT_PART
from yacut import app, db
from yacut.errors import InvalidAPIUsage
from yacut.forms import URLMapForm
from yacut.models import (URLMap, check_original_url, check_short_url,
                          get_unique_short_id)


@app.route("/api/id/", methods=["GET"])
def index_api_view():
    form = URLMapForm()
    return render_template("index.html", form=form), 200


@app.route("/api/id/", methods=["POST"])
def url_view():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage("Отсутствует тело запроса", status_code=400)

    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', status_code=400)

    data["url"] = check_original_url(data["url"])
    if "custom_id" not in data or not data["custom_id"]:
        data["custom_id"] = get_unique_short_id()

    data["custom_id"] = check_short_url(data["custom_id"])
    if URLMap.query.filter_by(short=data["custom_id"]).first() is not None:
        return (
            jsonify(
                {"message": "Предложенный вариант короткой ссылки уже существует."}
            ),
            400,
        )

    url = URLMap(original=data["url"], short=data["custom_id"])
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()

    if data["custom_id"].startswith(PERMANENT_PART):
        short_link = data["custom_id"]
    else:
        short_link = PERMANENT_PART + data["custom_id"]

    return jsonify({"url": data["url"], "short_link": short_link}), 201


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_full_url(short_id):
    url = URLMap.query.filter_by(short=short_id)
    if not url.all():
        return jsonify({"message": "Указанный id не найден"}), 404

    assert len(url.all()) == 1

    return jsonify({"url": url.first().original}), 200
