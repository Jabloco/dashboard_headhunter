import matplotlib.pyplot as plt
from io import BytesIO
import base64

import numpy as np
from pycbrf import ExchangeRates
from sqlalchemy import case, and_, not_, func

from app.models import Vacancy
from app import db


usd_rate = ExchangeRates()["USD"].rate
eur_rate = ExchangeRates()["EUR"].rate

def create_salaries(level: str):
    """
    Создает словарь с ключами в виде зарплат 
    и значениями в виде количества вакансий с такой зарплатой.

    Аргументы:
        level - уровень вакансии.
    """
    salaries = {}
    # Создаем case содержащий ЗП для каждой вакансии, исключая вакансии без ЗП.
    total_salary = case(
    [
        (and_(Vacancy.salary_from != None, Vacancy.salary_to != None), (Vacancy.salary_from + Vacancy.salary_to) / 2),
        (Vacancy.salary_from == None, Vacancy.salary_to),
        (Vacancy.salary_to == None, Vacancy.salary_from),
        (Vacancy.salary_to == None, Vacancy.salary_from),
    ],
    ).label("total_salary")

    # Создаем case содержащий ЗП для каждой вакансии в RUR.
    total_salary_rur = case(
        [
            (Vacancy.currency_id == "USD", total_salary * usd_rate),
            (Vacancy.currency_id == "EUR", total_salary * usd_rate),
        ],
    ).label("total_salary_rur")

    # Делаем запрос в БД и получаем данные о ЗП вакансий и о количестве повторяющихся ЗП.
    vacancies = db.session.query(
        Vacancy, func.count("total_salary"), total_salary_rur, total_salary
    ).filter(
        Vacancy.level == level
    ).filter(
        not_(
            and_(
                Vacancy.salary_from == None, 
                Vacancy.salary_to == None
            )
        )
    ).group_by("total_salary").all()

    for vacancy in vacancies:
        if vacancy.total_salary_rur is not None:
            salaries[vacancy.total_salary_rur] = vacancy[1]
        else:
            salaries[vacancy.total_salary] = vacancy[1]
    return salaries

def create_sorted_salaries(salaries: dict):
    """Создает список из количества вакансий по разным диапазонам зарплат."""
    sorted_salaries = [0, 0, 0]
    for salary in salaries.keys():
        if salary <= 100000:
            sorted_salaries[0] += salaries[salary]
        if salary > 100000 and salary < 200000:
            sorted_salaries[1] += salaries[salary]
        else:
            sorted_salaries[2] += salaries[salary]
    return sorted_salaries

def dash_link(create_dashboard: function):
    """
    Создает ссылку на изображение для вставки в шаблон html.

    Аргументы:
        create_dashboard - функция создания диаграммы.
    """
    fig = create_dashboard

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f'data:image/png;base64,{data}'

def create_pie_dashboard(levels_count: dict):
    """
    Функция принимает словарь вида {'junior': count, 'middle': count, 'senior': count}
    """
    labels = 'junior', 'middle', 'senior'
    sizes = [levels_count[label] for label in labels]

    figure, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100),  # счетчик вместо процентов
        shadow=True,
        startangle=90
    )

    return figure

def create_salary_dashboard(
    junior_salaries: dict,
    middle_salaries: dict,
    senior_salaries: dict):
    """
    Создает диаграмму зарплат по уровням.

    Аргументы:
        salary_dict - словарь с ключами в виде зарплат
        и значениями в виде количества вакансий с такой зарплатой.
    """
    junior_salary = create_sorted_salaries(junior_salaries)
    middle_salary = create_sorted_salaries(middle_salaries)
    senior_salary = create_sorted_salaries(senior_salaries)
        
    category_names = ["less than 100k", "100k - 200k", "200k and more"]
    results = {
        "Junior": junior_salary,
        "Middle": middle_salary,
        "Senior": senior_salary
    }
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(np.linspace(0.15, 0.85, data.shape[1]))
    # Размер горизонтальных колонок (ширина, высота).
    figure, ax = plt.subplots(figsize=(9, 5))
    ax.invert_yaxis()
    # Видимость шкалы по оси X.
    ax.xaxis.set_visible(True)
    # Значения шкалы по оси X.
    ax.set_xlim(-1, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
            loc='lower left', fontsize='small')
    ax.set_xlabel("Количество вакансий")

    return figure
