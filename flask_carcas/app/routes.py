from datetime import date, datetime
from flask.helpers import url_for
from flask import render_template, flash, redirect, request

from app import app
from app.models import Vacancy
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
    return render_template("keyskills.html", title="Ключевые навыки", page_text=page_text)

@app.route("/salary")
def salary():
    page_text = "Распределение зарплат"
    return render_template("salary.html", title="Распределение зарплат", page_text=page_text)


def levels_counts(date_from, date_to):
    """
    Функция делает запрос у БД с фильтрами по дате и уровню
    """
    levels = ['JUNIOR', 'MIDDLE', 'SENIOR', 'UNDEFINED']
    levels_counts = {
        level_name: Vacancy.query.filter(Vacancy.created_at>=date_from).filter(Vacancy.created_at<=date_to).filter_by(level=level_name).count() for level_name in levels
        }
    return levels_counts

@app.route("/vacancies", methods=["GET"])
def vacancies():
    """При вводе даты передает значения в переменные date_from, date_to."""
    page_text = "Количество вакансий по уровням"

    """
    Пытаемся получить данные через GET и привести их в формат даты.
    Если не получилось(например пустое поле) подставляем дефолтные значения.
    """
    try:
        date_from = datetime.strptime(request.args.get("date_from"), '%Y-%m-%d').date()
    except ValueError:
        date_from = datetime.strptime('2021-01-01', '%Y-%m-%d').date()

    try:
        date_to = datetime.strptime(request.args.get("date_to"), '%Y-%m-%d').date()
    except ValueError:
        date_to = date.today()

    image = dash_link(create_pie_dashboard(levels_counts(date_from, date_to)))

    # flash(f"Выбранная дата: c {date_from} до {date_to}.", 'message')
    return render_template("vacancies.html",title="Количество вакансий по уровням", page_text=page_text, image=image)
