from flask import jsonify, render_template, request

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import add_perm_in_short, get_validated_data


@app.route("/api/id/", methods=["GET"])
def index_api_view():
    form = URLMapForm()
    return render_template("index.html", form=form), 200


@app.route("/api/id/", methods=["POST"])
def url_view():
    data = request.get_json()
    get_validated_data(data)
    url = URLMap(original=data["url"], short=data["custom_id"])
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    short_link = add_perm_in_short(url.short)

    return jsonify({"url": data["url"], "short_link": short_link}), 201


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_full_url(short_id):
    url = URLMap.query.filter_by(short=short_id)
    if not url.all():
        return jsonify({"message": "Указанный id не найден"}), 404

    assert len(url.all()) == 1

    return jsonify({"url": url.first().original}), 200
