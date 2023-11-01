from datetime import datetime

from flask import url_for

from settings import ORIGINAL_LINK_LEN, SHORT_LINK_LEN
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original = db.Column(db.String(ORIGINAL_LINK_LEN), nullable=False)
    short = db.Column(db.String(SHORT_LINK_LEN))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for("get_original_url", short_id=self.short, _external=True),
        )

    def from_dict(self, data):
        self.original = data["url"]
        self.short = data["custom_id"]

    def __repr__(self):
        return "<URLMap {}>".format(self.original)
