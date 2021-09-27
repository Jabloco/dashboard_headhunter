from flask.helpers import url_for
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    page_text = "Привет!"
    return render_template("index.html", title="Home", page_text=page_text)

@app.route("/dash")
def dash():
    return render_template("dash.html", title="dash")

@app.route("/vacancy", methods=["GET", "POST"])
def vacancy():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Показана статистика по вакансии: {form.vacancy_name.data}.")
        return redirect(url_for("dash"))
    return render_template("vacancy_search.html", title="Dashboard", form=form)

