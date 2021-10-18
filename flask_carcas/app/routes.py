from flask.helpers import url_for
from flask import render_template, flash, redirect, request

from app import app
from app.forms import LoginForm
from app.dashboards import create_pie_dashboard, dash_link

@app.route("/")
@app.route("/index")
def index():
    page_text = "Привет!"
    return render_template("index.html", title="О проекте", page_text=page_text)

@app.route("/keyskills")
def keyskills():
    page_text = "Ключевые навыки"
    return render_template("index.html", title="Ключевые навыки", page_text=page_text)

@app.route("/salary")
def salary():
    page_text = "Распределение зарплат"
    return render_template("index.html", title="Распределение зарплат", page_text=page_text)

@app.route("/vacancies", methods=["GET"])
def vacancies():
    """При вводе даты передает значения в переменные date_from, date_to."""
    image = dash_link(create_pie_dashboard)
    date_from = request.args.get("date_from")
    date_to  = request.args.get("date_to")
    flash(f"Выбранная дата: c {date_from} до {date_to}.")
    return render_template("vacancies.html", image=image)
