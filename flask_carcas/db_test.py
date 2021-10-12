# from app import db
from app.models import Employer
from app.models import employer_insert
from api_client import HeadHunterClient

# db.create_all()

hh = HeadHunterClient()

vacancy_data = hh.get_vacancies_detail(36276899)
employer_insert(vacancy_data)
read = Employer.query.all()
print(read)