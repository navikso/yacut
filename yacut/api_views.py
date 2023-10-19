import random
from flask import jsonify, request, render_template
from . import app, db
# from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .forms import URLMapForm
from settings import CHARACTERS, PERMANENT_PART
from wtforms import ValidationError
from .views import random_url

# @app.route('/api/id/', methods=['POST'])
# def add_short_url():
#     data = request.get_json()
# #     if 'short' in data:
# #         raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
#
#
#     url = random_url()
#     db.session.add(url)
#     db.session.commit()
#     return jsonify({'url': url.to_dict()}), 201

@app.route('/api/id/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():

        try:
            url = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data,
            )
        except TypeError:
            raise ValidationError("Wrong JSON data format", 401)
        if url.short is not None:
            # if URLMap.query.filter_by(short=url.short) is not None:
            #     raise ValueError('Такой короткий url уже зарегистрирован')
            return render_template('index.html', form=form, short=url.short)
        url = random_url()
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, short=url)
    return render_template('index.html', form=form)


@app.route('/api/id/', methods=['POST'])
def add_url():
    characters = list(CHARACTERS)
    data = request.get_json()
    random.shuffle(characters)
    short_gen = ''.join([random.choice(CHARACTERS) for x in range(6)])
    url = PERMANENT_PART + short_gen
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()

    return jsonify({'url': url.to_dict()}), 201


@app.route('/api/id/<int:id>/', methods=['GET'])
def get_full_url(id):
    url = URLMap.query.get_or_404(id)
    return render_template('full_url.html', url=url.original)


if __name__ == '__main__':
    app.run()
