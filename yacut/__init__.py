from flask import Flask
from settings import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../html/',
    template_folder='../html/',
)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import cli_commands, models, errors, views, api_views, forms


if __name__ == '__main__':
    app.run()
