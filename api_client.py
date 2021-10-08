import logging
import requests


from flask_carcas.app import db
from constants import Levels


logging.basicConfig(format='%(levelname)s - %(message)s',
                    filename='error.log')

class HeadHunterClient:
    API_BASE_URL = 'https://api.hh.ru/'
    VACANCIES_LIST_PATH = 'vacancies/'

    def __init__(self):
        pass

    def get_vacancies_ids(self, vacancy_name, page, area=1) -> list:
        """Метод получения списка из id вакансий на странице.

        Возвращает список.
        Аргументы:
            vacancy_name - название требуемой вакансии
            page - номер страницы
            area - регион, по умолчанию = 1 (Москва)
        """
        params = {
            "area": area,
            "st": "searchVacancy",
            "text": vacancy_name,
            "page": page,
            "per_page": 100  # Параметр ограничен значением в 100 (из документации).
            }

        try:
            result = requests.get(f'{self.API_BASE_URL}{self.VACANCIES_LIST_PATH}', params=params)
        except requests.RequestException as error:
            logging.exception(error)
            return
        result.raise_for_status()
        vacancy_page = result.json()
        if 'errors' in vacancy_page:
            raise ValueError('Запрос не выполнен')
        vacancy_ids = [vacancy["id"] for vacancy in vacancy_page["items"]]
        return vacancy_ids
            
    def get_vacancies_level(self, vacancy_id) -> str:
        """ Метод получения уровня сосискателя (Junior, Middle, Senior) для вакансии

        Возвращает строку.
        Аргументы:
            vacancy_id - id вакансии
        """
        vacancy_sections = ["name", "description"]
        vacancy_level = Levels.UNDEFINED.name

        # проверяем входные данные
        try:
            vacancy_id = int(vacancy_id)
        except TypeError as error:
            logging.exception(error)
            return
        except ValueError as error:
            logging.exception(error)
            return
        try:
            result = requests.get(f'{self.API_BASE_URL}{self.VACANCIES_LIST_PATH}{vacancy_id}')
        except requests.RequestException as error:
            logging.exception(error)
            return
        result.raise_for_status()
        vacancy_page = result.json()
        if 'errors' in vacancy_page:
            raise ValueError('Запрос не выполнен')
        for section in vacancy_sections:
            for level in Levels:
                for similiar_level in level.value:
                    if similiar_level in vacancy_page[section].lower():
                        vacancy_level = level.name
        return vacancy_level

    def get_vacancies_detail(self, vacancy_id) -> dict:
        """
        Метод для получения нужной информации о вакансии.

        Аргументы:
            vacancy_id - id вакансии
        Возвращает словарь.
        """
        
        # проверяем входные данные
        try:
            vacancy_id = int(vacancy_id)
        except TypeError as error:
            logging.exception(error)
            return
        except ValueError as error:
            logging.exception(error)
            return

        params = {
            'host': 'hh.ru'
        }

        # делаем запрос
        try:
            req = requests.get(f'{self.API_BASE_URL}{self.VACANCIES_LIST_PATH}{vacancy_id}', params)
            answer = req.json()  # декодируем и приводим к питоновскому словарю
            req.raise_for_status()
            if 'errors' in answer:
                raise ValueError('Запрос не выполнен')
        except ValueError as error:
            logging.exception(error)
            return
        except requests.RequestException as error:
            logging.exception(error)
            return

        # формируем словарь 
        data = {
            'hh_id': answer['id'],
            'name': answer['name'],
            'area_id': answer['area']['id'],
            'area_name': answer['area']['name'],
            'experience_id': answer['experience']['id'],
            'schedule_id': answer['schedule']['id'],
            'employment_id': answer['employment']['id'],
            'key_skills': answer['key_skills'],
            'employer_id': answer['employer']['id'],
            'employer_name': answer['employer']['name'],
            'employer_url': answer['employer']['url'],
            'created_at': answer['created_at']
        }
        # проверяем зарплату и дополняем словарь
        if answer['salary'] is None:
            data.update(
                {
                    'salary_from': None,
                    'salary_to': None,
                    'currency': None
                }
            )
        else:
            data.update(
                {
                    'salary_from': answer['salary']['to'],
                    'salary_to': answer['salary']['to'],
                    'currency': answer['salary']['currency']
                }
            )

        return data

if __name__ == '__main__':
    pass
    