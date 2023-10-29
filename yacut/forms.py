from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from settings import MIN_LEN, ORIGINAL_LINK_LEN, SHORT_LINK_LEN


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Введите ссылку",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(MIN_LEN, ORIGINAL_LINK_LEN),
        ],
    )
    custom_id = URLField(
        "Введите свой вариант короткой ссылки",
        validators=[Length(MIN_LEN, SHORT_LINK_LEN), Optional()],
    )
    submit = SubmitField("Создать")
