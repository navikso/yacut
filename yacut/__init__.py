from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../html/",
    template_folder="../html/",
)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import api_views, errors, forms, models, views

if __name__ == "__main__":
    app.run()
