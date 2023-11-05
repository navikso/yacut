import random

from yacut import db
from yacut.models import URLMap
from yacut.validators import get_validated_data


def get_url_by_id_or_404(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()

    return url.original


def get_short_link(data):
    get_validated_data(data)
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()

    return urlmap.to_dict()
