import logging
import requests


logging.basicConfig(format='%(levelname)s - %(message)s',
                    filename='error.log')

class HeadHunterClient:
    API_BASE_URL = 'https://api.hh.ru/'
    VACANCIES_LIST_PATH = 'vacancies/'

    def __init__(self):
        pass
        
    def get_vacancys_list(self):
       pass            
        
    def get_vacancy_detail(self, vacancy_id) -> dict:
        """
        Метод для получения нужной информации о вакансии\n
        Аргументы:\n
            vacancy_id - id вакансии\n
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