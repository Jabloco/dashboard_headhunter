from datetime import date, datetime

from flask import render_template, request

from app import app
from app.models import Vacancy
from app.dashboards import create_pie_dashboard, dash_link


def levels_counts(date_from, date_to):
    """
    Функция делает запрос у БД с фильтрами по дате и уровню
    """
    levels = ['JUNIOR', 'MIDDLE', 'SENIOR', 'UNDEFINED']
    levels_counts = {
        level_name: Vacancy.query.filter(Vacancy.created_at>=date_from).filter(Vacancy.created_at<=date_to).filter_by(level=level_name).count() for level_name in levels
        }
    return levels_counts


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


@app.route("/vacancies", methods=["GET"])
def vacancies():
    """
    При вводе даты передает значения в переменные date_from, date_to.
    Пытаемся получить данные через GET и привести их в формат даты.
    Если не получилось(например пустое поле) подставляем дефолтные значения.
    """
    try:
        get_date_from = request.args.get("date_from")
        if get_date_from is None:
            raise ValueError
        date_from = datetime.strptime(get_date_from, '%Y-%m-%d').date()
    except ValueError:
        date_from = datetime.strptime('2021-01-01', '%Y-%m-%d').date()

    try:
        get_date_to = request.args.get("date_to")
        if get_date_to is None:
            raise ValueError
        date_to = datetime.strptime(get_date_to, '%Y-%m-%d').date()
    except ValueError:
        date_to = date.today()

    image = dash_link(create_pie_dashboard(levels_counts(date_from, date_to)))

    return render_template("vacancies.html",title="Количество вакансий по уровням", image=image)
