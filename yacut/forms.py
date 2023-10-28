from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from settings import ORIGINAL_LINK_LEN, SHORT_LINK_LEN


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Введите ссылку",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(1, ORIGINAL_LINK_LEN),
        ],
    )
    custom_id = URLField(
        "Введите свой вариант короткой ссылки",
        validators=[Length(1, SHORT_LINK_LEN), Optional()],
    )
    submit = SubmitField("Создать")
