from flask import jsonify, render_template, request

from yacut import app, db
from yacut.errors import InvalidAPIUsage
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import add_perm_in_short, get_validated_data, get_unique_short_id, get_url_by_id_or_404


@app.route("/api/id/", methods=["GET"])
def index_api_view():
    form = URLMapForm()
    return render_template("index.html", form=form), 200

    # try:
    #     get_validated_data(request.get_json())
    #     return jsonify(get_unique_short_id()), 201
    # except Exception as err:
    #     raise InvalidAPIUsage(str(err), status_code=400)



@app.route("/api/id/", methods=["POST"])
def get_short_url():
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
    try:
        url = get_url_by_id_or_404(short_id)
        return jsonify({"url": url}), 200
    except:
        return jsonify({"message": "Указанный id не найден"}), 404
