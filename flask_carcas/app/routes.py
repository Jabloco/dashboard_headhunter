from flask.helpers import url_for
from flask import render_template, flash, redirect

from app import app
from app.forms import LoginForm
from app.dashboards import create_pie_dashboard, dash_link

@app.route("/")
@app.route("/index")
def index():
    page_text = "Привет!"
    return render_template("index.html", title="Home", page_text=page_text)

@app.route("/pie_dash")
def dash():
    image = dash_link(create_pie_dashboard)
    return render_template("pie_dash.html", image=image)

@app.route("/vacancy", methods=["GET", "POST"])
def vacancy():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Показана статистика по вакансии: {form.vacancy_name.data}.")
        return redirect(url_for("pie_dash"))
    return render_template("vacancy_search.html", title="Dashboard", form=form)

