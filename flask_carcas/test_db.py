# from app import app
from app.models import Vacancy


date_from = '2021-10-04'
date_to = '2021-10-20'
levels = ['JUNIOR', 'MIDDLE', 'SENIOR', 'UNDEFINED']
levels_counts = {level_name: Vacancy.query.filter_by(level = level_name).count() for level_name in levels}
print(levels_counts)

levels_counts = {level_name: Vacancy.query.filter(Vacancy.created_at>=date_from).filter(Vacancy.created_at<=date_to).filter_by(level=level_name).count() for level_name in levels}
print(levels_counts)
