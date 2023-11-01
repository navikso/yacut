from flask import jsonify, request

from yacut import app
from yacut.errors import InvalidAPIUsage
from yacut.services import get_short_link, get_url_by_id_or_404


@app.route("/api/id/", methods=["POST"])
def get_short_url():
    try:
        return jsonify(get_short_link(request.get_json())), 201
    except Exception as err:
        raise InvalidAPIUsage(str(err), status_code=400)


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_full_url(short_id):
    try:
        return jsonify({"url": get_url_by_id_or_404(short_id)}), 200
    except Exception:
        return jsonify({"message": "Указанный id не найден"}), 404
