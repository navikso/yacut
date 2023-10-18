import random
# from urllib.parse import urljoin
from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import URLField
from wtforms.validators import DataRequired, Length, Optional


CHARACTERS = '123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
PERMANENT_PART = 'http://127.0.0.1:5000/'


app = Flask(__name__,
            static_url_path='',
            static_folder='./html/',
            template_folder='./html/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123qwe123'

db = SQLAlchemy(app)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = URLField(
        'Введите свой вариант короткой ссылки',
    )


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    characters = list(CHARACTERS)
    if form.validate_on_submit():
        url = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        if url.short is not None:
            return render_template('index.html', form=form, short=url.short)
        random.shuffle(characters)
        short_gen = ''.join([random.choice(CHARACTERS) for x in range(6)])
        url = PERMANENT_PART + short_gen
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, short=url)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
