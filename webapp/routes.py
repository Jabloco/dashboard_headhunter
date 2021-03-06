from datetime import date, datetime

from flask import render_template, request, flash
from sqlalchemy import func, desc

from webapp import hh_app
from webapp import db
from webapp.models import KeySkill, Vacancy, vacancy_skill
from webapp.dashboards import (create_pie_dashboard, create_salary_dashboard, create_salaries, create_keyskills_dashboard, dash_link)
from constants import Levels


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


def keyskills_count(date_from, date_to, keyskills: list):
    """
    Функция для подсчета навыков.
    Параметры:
        date_from - дата фильтрации от
        date_to - дата фильтрации до
        keyskills - список навыков которые интересуют. Если список не передается,
        то возвращается 20 самых частоупоминаемых навыков
    """
    query_base = db.session.query(
        KeySkill.name, func.count(vacancy_skill.c.keyskill_id).label('total')
    ).join(
        vacancy_skill
    ).join(
        Vacancy
    ).group_by(
        KeySkill.name
    ).filter(
        Vacancy.created_at.between(date_from, date_to)
    ).order_by(
        desc('total')
    )

    if keyskills:
        query_skills_counts = query_base.filter(
            KeySkill.name.in_(keyskills)
        )
    else:
        query_skills_counts = query_base.limit(20)

    skill_counts = dict(query_skills_counts.all())
    return skill_counts


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


@hh_app.route("/")
@hh_app.route("/index")
def index():
    page_text = "Привет!"
    return render_template("index.html", title="О проекте", page_text=page_text)


@hh_app.route("/keyskills", methods=["GET"])
def keyskills():
    """
    Вывод столбчатой диаграммы по ключевым навыкам
    """
    get_date_from = request.args.get("date_from")
    get_date_to = request.args.get("date_to")
    get_skills = request.args.getlist("skills[]")

    date_from, date_to = get_date(get_date_from, get_date_to)  # проверка и преобразование дат
    raw_skills = db.session.query(KeySkill.name.distinct()) # получение списка всех скилов
    skills = [skill[0] for skill in raw_skills]

    image = dash_link(create_keyskills_dashboard(keyskills_count(date_from, date_to, get_skills)))
    
    date_to_str = date_to.strftime('%d.%m.%Y')
    date_from_str = date_from.strftime('%d.%m.%Y')
    if not get_date_from and not get_date_to:
        flash("Данные за все время:")
    elif not get_date_from:
        flash(f"Данные по {date_to_str}:")
    elif not get_date_to:
        flash(f"Данные с {date_from_str}:")
    else:
        flash(f"Данные с {date_from_str} по {date_to_str}:")

    return render_template(
        "keyskills.html",
        title="Ключевые навыки",
        image=image,
        skills=skills
        )

@hh_app.route("/salary", methods=["GET"])
def salary():
    page_text = "Распределение зарплат"
    image = dash_link(create_salary_dashboard(
        create_salaries(Levels.JUNIOR.name),
        create_salaries(Levels.MIDDLE.name),
        create_salaries(Levels.SENIOR.name)))
    return render_template("salary.html", title="Распределение зарплат", page_text=page_text, image=image)


@hh_app.route("/vacancies", methods=["GET"])
def vacancies():
    """
    Вывод круговой диаграммы со счетчиком вакансий по уровням
    """
    get_date_from = request.args.get("date_from")
    get_date_to = request.args.get("date_to")

    date_from, date_to = get_date(get_date_from, get_date_to)  # проверка и преобразование дат

    date_to_str = date_to.strftime('%d.%m.%Y')
    date_from_str = date_from.strftime('%d.%m.%Y')
    if not get_date_from and not get_date_to:
        flash("Данные за все время:")
    elif not get_date_from:
        flash(f"Данные по {date_to_str}:")
    elif not get_date_to:
        flash(f"Данные с {date_from_str}:")
    else:
        flash(f"Данные с {date_from_str} по {date_to_str}:")

    image = dash_link(create_pie_dashboard(levels_counts(date_from, date_to)))

    return render_template("vacancies.html", title="Количество вакансий по уровням", image=image)
