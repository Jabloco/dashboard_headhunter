import json

import requests
from requests.models import Request


class Headhunter:
    def __init__(self):
        pass
        
    def GetVacancysList(self):
       pass            
        
    def GetVacancyDetail(self, vacancy_id):
        """
        Метод для получения нужной информации о вакансии\n
        Аргументы:\n
            vacancy_id - id вакансии
        """
        # проверяем входные данные
        try:
            vacancy_id = int(vacancy_id)
        except TypeError as error:
            print('Неверный параметр', error)
            return
        except ValueError as error:
            print('Проверьте id', error)
            return

        # делаем запрос
        self.vacancy_id = vacancy_id
        try:
            self.req = requests.get(f'https://api.hh.ru/vacancies/{self.vacancy_id}?host=hh.ru')
            self.answer = json.loads(self.req.content.decode())  # декодируем и приводим к питоновскому словарю
            self.req.raise_for_status
            self.req.close()
            if 'errors' in self.answer:
                raise ValueError('Запрос не выполнен')
        except ValueError as error:
            print(error)
            return
        except requests.ConnectionError as error:
            print('Ошибка подключения', error)
            return

        # формируем словарь 
        self.data = {'hh_id': self.answer['id'],
                        'name': self.answer['name'],
                        'area_id': self.answer['area']['id'],
                        'area_name': self.answer['area']['name'],
                        'experience_id': self.answer['experience']['id'],
                        'schedule_id': self.answer['schedule']['id'],
                        'employment_id': self.answer['employment']['id'],
                        'key_skills': self.answer['key_skills'],
                        'employer_id': self.answer['employer']['id'],
                        'employer_name': self.answer['employer']['name'],
                        'employer_url': self.answer['employer']['url'],
                        'created_at': self.answer['created_at']
                    }
        # проверяем зарплату и дополняем словарь
        if self.answer['salary'] is None:
            self.data.update({'salary_from': None,
                                'salaty_to': None,
                                'currency': None
                            })
        if self.answer['salary']:
            self.data.update({'salary_from': self.answer['salary']['to'],
                            'salaty_to': self.answer['salary']['to'],
                            'currency': self.answer['salary']['currency']
                            })

        return self.data

if __name__ == '__main__':
    hh_data = Headhunter()

    vac_id = 4452998
    print(hh_data.GetVacancyDetail(vac_id))
    vac_id = '44528998'
    print(hh_data.GetVacancyDetail(vac_id))
    vac_id = '44528ff998'
    print(hh_data.GetVacancyDetail(vac_id))
    vac_id = '445299811122'
    print(hh_data.GetVacancyDetail(vac_id))