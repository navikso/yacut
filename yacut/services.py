from yacut import db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.validators import (check_on_empty, check_original_url,
                              check_short_url)


def get_url_by_id_or_404(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()

    return url.original


def get_short_link(data):
    check_on_empty(data)
    check_original_url(data)

    if "custom_id" not in data or not data["custom_id"]:
        data["custom_id"] = get_unique_short_id()
    else:
        check_short_url(data)

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()

    return urlmap.to_dict()
