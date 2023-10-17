from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import randrange
from flask_wtf import FlaskForm
from wtforms import URLField
from wtforms.validators import DataRequired, Length, Optional


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


@app.route('/')
def index_view():
    form = URLMapForm()
    # quantity = URLMap.query.count()
    # if not quantity:
    #     return 'В базе данных мнений о фильмах нет.'
    # offset_value = randrange(quantity)
    # original_url = URLMap.query.offset(offset_value).first()
    # # Вот здесь в шаблон передаётся весь объект opinion
    return render_template('index.html', form=form)
    # , original_url=original_url)


if __name__ == '__main__':
    app.run()
