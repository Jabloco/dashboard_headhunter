from datetime import datetime

from app.models import Employer, Vacancy, KeySkill, Area, keyskill_vacancy
from api_client import HeadHunterClient
from constants import search_text


hh = HeadHunterClient()


def vacancies_ids(text: str, area_id: int) -> list:
    """
    Функция для получения максимально возможного
    количества (2000) вакансий на один запрос.

    """
    vacancies_ids_total = []
    for page in range(20):
        vacancies_ids_on_page, pages = hh.get_vacancies_ids(text, page, area_id)
        vacancies_ids_total.extend(vacancies_ids_on_page)
        if (pages - page) <= 1:
            return vacancies_ids_total


def write_to_db(vacancies_id):
    for id in vacancies_id:
        """
        Что бы не дергать api по каждой вакансии при повторном запуске
        сначала проверим есть ли уже вакансия с hh_id в локальной базе.
        Если нет то будем запрашивать детали вакансии.
        """
        is_vacancy_add = Vacancy.query.filter_by(hh_id=id).first()
        if is_vacancy_add is None:
            vacancy_detail = hh.get_vacancy_detail(id)
            
            area = Area.insert(vacancy_detail['area_id'], vacancy_detail['area_name'])
            employer = Employer.insert(vacancy_detail['employer_id'], vacancy_detail['employer_name'])

            vacancy_obj = Vacancy.insert(
                int(vacancy_detail['hh_id']),
                vacancy_detail['salary_from'],
                vacancy_detail['salary_to'],
                vacancy_detail['currency'],
                vacancy_detail['experience_id'],
                vacancy_detail['schedule_id'],
                vacancy_detail['employment_id'],
                int(area.id),
                int(employer.id),
                datetime.strptime(vacancy_detail['created_at'], '%Y-%m-%dT%H:%M:%S%z'),
                vacancy_detail['level']
            )

            # keyskills = [skill['name'] for skill in vacancy_detail['key_skills']]
            # keyskill_vacancy(vacancy_obj, keyskills)


areas_ids = hh.get_areas_ids()

for text in search_text:
    for area_id in areas_ids:
        print(text, area_id)
        vacancies_id = vacancies_ids(text, area_id)
        write_to_db(vacancies_id)
