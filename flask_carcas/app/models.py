import sqlalchemy.orm.exc
import logging

from os import name
import logging

from app import db
import sqlalchemy.orm.exc
from api_client import HeadHunterClient

logging.basicConfig(format='%(levelname)s - %(message)s',
                    filename='error.log')

vacancy_skill = db.Table('vacancy_skill',
    db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id'), primary_key=True),
    db.Column('keyskill_id', db.Integer, db.ForeignKey('keyskill.id'), primary_key=True)
)

def get_or_create(model, **kwargs):
    """
    Делаем запрос в БД, при наличии определенной записи,
    возвращаем ее, при отсутствии, создаем и возвращаем.
    """
    try:
        model_object = model.query.filter_by(**kwargs).first()
    # Лишний аргумент в запросе.
    except sqlalchemy.exc.InvalidRequestError as error:
        logging.exception(error)
        return None, None
    if model_object is not None:
        return model_object, False
    try:
        model_object = model(**kwargs)
        db.session.add(model_object)
        db.session.commit()
    # Один из аргументов Unique уже существует.
    except sqlalchemy.exc.IntegrityError as error:
        logging.exception(error)
        return None, None
    return model_object, True

class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'id: {self.id}, hh_id: {self.hh_id}, area_name: {self.name}'


class KeySkill(db.Model):
    __tablename__ = 'keyskill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    vacancies = db.relationship('Vacancy', secondary=vacancy_skill)

    def __repr__(self):
        return f'id: {self.id}, keyskill_name: {self.name}'


class Vacancy(db.Model):
    __tablename__ = 'vacancy'
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, unique=True, nullable=False)
    salary_from = db.Column(db.Integer)
    salary_to = db.Column(db.Integer)
    currency_id = db.Column(db.String(128))
    experience_id = db.Column(db.String(128))
    schedule_id = db.Column(db.String(128))
    employment_id = db.Column(db.String(128))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    level = db.Column(db.String(128), nullable=False)
    area = db.relationship('Area', backref='vacancies')
    employer = db.relationship('Employer', backref='vacancies')

    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}"


class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(128), unique=True)


    @classmethod
    def insert(cls, hh_id, name):
        employer = {
            'hh_id': hh_id,
            'name': name
        }
        row = get_or_create(Employer, **employer)
        return row


    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}, employer_name:{self.name}"





def keyskill_vacancy(vacancy_data: dict):
    """
    Функция для заполнения связующей таблицы М2М.
    Принимает словарь с данными о вакансии.
    Поскольку заполняется связующая таблица,
    то имеет смысл выполнять функцию
    после того как данные из словаря занесены
    в соответствующие таблицы, иначе нечего будет свызывать =)
    """
    vacancy_hh_id = vacancy_data['hh_id']
    key_skills = vacancy_data['key_skills']

    # находим id вакансии
    try:
        vacancy = Vacancy.query.filter_by(hh_id=vacancy_hh_id).first()
        vacancy_id = {'vacancy_id': vacancy.id}
    except sqlalchemy.exc.InvalidRequestError as error:
        logging.exception(error)
        return None

    # проходим по списку скилов и для каждого ищем id
    for keyskill in key_skills:
        vacancy_skill_ids = {}
        skill_name = keyskill['name']
        try:
            skill = KeySkill.query.filter_by(name=skill_name).first()
            skill_id = {'keyskill_id': skill.id}
        except sqlalchemy.exc.InvalidRequestError as error:
            logging.exception(error)
            return None

        if vacancy_id and skill_id:
            vacancy_skill_ids = {**vacancy_id, **skill_id}
            get_or_create(vacancy_skill, vacancy_skill_ids)