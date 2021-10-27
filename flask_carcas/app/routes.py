from flask import render_template

from app import app
from app.dashboards import create_salary_dashboard, create_salary_dict, dash_link

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
    image = dash_link(create_salary_dashboard(
        create_salary_dict("JUNIOR"),
        create_salary_dict("MIDDLE"),
        create_salary_dict("SENIOR")))
    return render_template("salary.html", title="Распределение зарплат", page_text=page_text, image=image)

@app.route("/vacancies")
def vacancies():
    page_text = "Количество вакансий по уровням"
    return render_template("vacancies.html", title="Количество вакансий по уровням", page_text=page_text)
