import random
from flask import abort, jsonify, request, render_template
from . import app, db
# from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .forms import URLMapForm
from settings import CHARACTERS, PERMANENT_PART
from wtforms import ValidationError


def random_url():
    characters = list(CHARACTERS)
    random.shuffle(characters)
    short_gen = ''.join([random.choice(CHARACTERS) for x in range(6)])
    url = PERMANENT_PART + short_gen
    return url

# @app.route('/api/id/')
# def index_view():
#     url = random_url()
#     if url is not None:
#         return render_template('url.html', url=url)
#     abort(404)
