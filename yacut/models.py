from datetime import datetime

from settings import ORIGINAL_LINK_LEN, SHORT_LINK_LEN
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original = db.Column(db.String(ORIGINAL_LINK_LEN), nullable=False)
    short = db.Column(db.String(SHORT_LINK_LEN), unique=True)
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
