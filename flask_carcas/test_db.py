# from app import app
from app.models import Vacancy

# j = Vacancy.query.filter_by(level = 'JUNIOR').count()
levels = ['JUNIOR', 'MIDDLE', 'SENIOR', 'UNDEFINED']
# levels = ['junior', 'middle', 'senior']
levels_counts = {level_name: Vacancy.query.filter_by(level = level_name).count() for level_name in levels}


print(levels_counts)
# print(j)