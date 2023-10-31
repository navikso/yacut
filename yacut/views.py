from flask import redirect, render_template

from settings import PERMANENT_PART
from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, get_validated_form, get_url_by_id_or_404


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        urlmap = URLMap(original=form.original_link.data, short=form.custom_id.data)
        get_validated_form(form, urlmap)
        if not urlmap.short:
            urlmap.short = get_unique_short_id()
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
    url = get_url_by_id_or_404(short_id)
    return redirect(url)
