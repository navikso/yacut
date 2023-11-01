from flask import flash, redirect, render_template

from yacut import app
from yacut.forms import URLMapForm
from yacut.services import get_short_link, get_url_by_id_or_404


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            get_short_link(
                {"url": form.original_link.data,
                 "custom_id": form.custom_id.data}
            )
            return (
                render_template(
                    "index.html",
                    form=form,
                    short=form.custom_id.data,
                    original=form.original_link.data,
                ),
                200,
            )
        except Exception as err:
            flash(str(err))
    return render_template("index.html", form=form), 200


@app.route("/<string:short_id>", methods=["GET"])
def get_original_url(short_id):
    return redirect(get_url_by_id_or_404(short_id))
