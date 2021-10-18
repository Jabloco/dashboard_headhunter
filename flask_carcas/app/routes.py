from flask.helpers import url_for
from flask import render_template, flash, redirect, request

from app import app
from app.forms import LoginForm
from app.dashboards import create_pie_dashboard, dash_link

@app.route("/")
@app.route("/index")
def index():
    page_text = "Привет!"
    return render_template("index.html", title="Home", page_text=page_text)

@app.route("/pie_dash", methods=["GET"])
def dash():
    """При вводе даты передает значения в переменные date_from, date_to."""
    image = dash_link(create_pie_dashboard)
    date_from = request.args.get("date_from")
    date_to  = request.args.get("date_to")
    flash(f"Выбранная дата: c {date_from} до {date_to}.")
    return render_template("pie_dash.html", image=image)

@app.route("/vacancy", methods=["GET", "POST"])
def vacancy():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Показана статистика по вакансии: {form.vacancy_name.data}.")
        return redirect(url_for("dash"))
    return render_template("vacancy_search.html", title="Dashboard", form=form)

