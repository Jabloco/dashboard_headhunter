import matplotlib.pyplot as plt
from io import BytesIO
import base64

import numpy as np

from app.models import Vacancy


def create_salary_dict(level: str):
    """
    Создает словарь с ключами в виде зарплат 
    и значениями в виде количества вакансий с такой зарплатой.

    Аргументы:
        level - уровень вакансии.
    """
    # Делаем запрос в БД и получаем все вакансии с уровня "level".
    vacancies = Vacancy.query.filter(Vacancy.level==level).all()
    salary_dict = {}
    for vacancy in vacancies:
        # При отсутствии значений "salary_from" или "salary_to" берем существующее.
        if vacancy.salary_from == None and vacancy.salary_to == None:
            continue
        elif vacancy.salary_from == None:
            salary = vacancy.salary_to 
        elif vacancy.salary_to == None:
            salary = vacancy.salary_from
        else:
            salary = (vacancy.salary_from + vacancy.salary_to) / 2
        # При значении "currency" отличного от "RUR" переводим значение в "RUR".
        if vacancy.currency_id == "USD":
            salary *= 70
        if vacancy.currency_id == "EUR":
            salary *= 81
        if salary not in salary_dict:
            salary_dict[salary] = 1
        else:
            salary_dict[salary] += 1
    return salary_dict

def create_salary_list(salary_dict):
    """Создает список из количества вакансий по разным диапазонам зарплат."""
    salary_list = [0, 0, 0]
    for salary in salary_dict.keys():
        if salary <= 100000:
            salary_list[0] += salary_dict[salary]
        if salary > 100000 and salary < 200000:
            salary_list[1] += salary_dict[salary]
        else:
            salary_list[2] += salary_dict[salary]
    return salary_list

def dash_link(create_dashboard):
    """
    Создает ссылку на изображение для вставки в шаблон html.

    Аргументы:
        create_dashboard - функция создания диаграммы.
    """
    fig = create_dashboard()

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
    salary_dict_junior,
    salary_dict_middle,
    salary_dict_senior):
    """
    Создает диаграмму зарплат по уровням.

    Аргументы:
        salary_dict - словарь с ключами в виде зарплат
        и значениями в виде количества вакансий с такой зарплатой.
    """
    junior_salary = create_salary_list(salary_dict_junior)
    middle_salary = create_salary_list(salary_dict_middle)
    senior_salary = create_salary_list(salary_dict_senior)
        
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
