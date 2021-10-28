from datetime import date, datetime

from flask import render_template, request
from sqlalchemy import func

from app import app
from app import db
from app.models import Vacancy
from app.dashboards import create_pie_dashboard, dash_link


def levels_counts(date_from, date_to):
    """
    Функция делает запрос у БД с фильтрами по дате и уровню
    """
    levels_counts = db.session.query(
        Vacancy.level, func.count(Vacancy.level)
        ).group_by(
            Vacancy.level
        ).filter(
            Vacancy.created_at.between(date_from, date_to)
        ).all()
    counts = dict(levels_counts)
    return counts


def get_date(get_date_from, get_date_to):
    """
    Поскольку фильтация по дате присутствует на всех страницах,
    то вынес преобразование результата GET-запроса даты в отдельную функцию.

    Проверяем входящие данные (не пустые ли) и в зависимости от результата
    подставляем либо дефолтное значение, либо введеную дату.

    В случае если введенная дата начала позже даты окончания
    тоже подставляем дефолтные значения
    """
    if get_date_from == '' or get_date_from is None:
        date_from = datetime(2021, 1, 1).date()
    else:
        date_from = datetime.strptime(get_date_from, '%Y-%m-%d').date()

    if get_date_to == '' or get_date_to is None:
        date_to = date.today()
    else:
        date_to = datetime.strptime(get_date_to, '%Y-%m-%d').date()

    if date_from > date_to:
        date_from = datetime(2021, 1, 1).date()
        date_to = date.today()

    return date_from, date_to


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
    Вывод круговой диаграммы со счетчиком вакансий по уровням
    """
    get_date_from = request.args.get("date_from")
    get_date_to = request.args.get("date_to")

    date_from, date_to = get_date(get_date_from, get_date_to)  # проверка и преобразование дат

    image = dash_link(create_pie_dashboard(levels_counts(date_from, date_to)))

    return render_template("vacancies.html", title="Количество вакансий по уровням", image=image)
