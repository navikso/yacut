from flask import flash, redirect, render_template

from settings import PERMANENT_PART, SPECIAL_CHARS
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap, get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        urlmap = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        if not urlmap.short:
            urlmap.short = get_unique_short_id()

        if any(char in SPECIAL_CHARS for char in urlmap.short):
            flash("Указано недопустимое имя для короткой ссылки")
            return render_template("index.html", form=form), 400

        if URLMap.query.filter_by(short=urlmap.short).first() is not None:
            flash("Предложенный вариант короткой ссылки уже существует.")
            return render_template("index.html", form=form), 400

        db.session.add(urlmap)
        db.session.commit()

        return (
            render_template(
                "index.html",
                form=form,
                short=PERMANENT_PART + urlmap.short,
                original=urlmap.original,
            ),
            200,
        )

    return render_template("index.html", form=form), 200


@app.route("/<string:short_id>", methods=["GET"])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        return render_template("404.html"), 404

    return redirect(url.original)
