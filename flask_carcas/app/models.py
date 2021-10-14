import sqlalchemy.orm.exc
import logging

from os import name
from app import db

vacancy_skill = db.Table('vacancy_skill',
    db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id'), primary_key=True),
    db.Column('keyskill_id', db.Integer, db.ForeignKey('keyskill.id'), primary_key=True)
)

def get_or_create(model, **kwargs):
    """
    Делает запрос в БД, при наличии определенной записи,
    возвращает ее, при отсутствии, создаем и возвращаем.
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

    def insert(self, vacancy_data):
        """Записывает данные в таблицу Area."""
        area = {"hh_id": vacancy_data['area_id'], "name": vacancy_data['area_name']}
        get_or_create(Area, **area)

    def __repr__(self):
        return f'id: {self.id}, hh_id: {self.hh_id}, area_name: {self.name}'


class KeySkill(db.Model):
    __tablename__ = 'keyskill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    vacancies = db.relationship('Vacancy', secondary=vacancy_skill)

    def insert(self, vacancy_data):
        """Записывает данные в таблицу KeySkill."""
        key_skill = {"name": vacancy_data['key_skills']}
        get_or_create(KeySkill, **key_skill)

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
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'),nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'),nullable=False) 
    created_at = db.Column(db.Date, nullable=False)
    level = db.Column(db.String(128), nullable=False)
    area = db.relationship('Area', backref='vacancies')
    employer = db.relationship('Employer', backref='vacancies')

    @classmethod
    def insert(cls):
        """Записывает данные в таблицу Vacancy."""
        vacancy = {
            "hh_id": cls.id["hh_id"],
            "salary_from": vacancy_data["salary_from"],
            "salary_to": vacancy_data["salary_to"],
            "currency_id": vacancy_data["currency"],
            "experience_id": vacancy_data["experience_id"],
            "schedule_id": vacancy_data["schedule_id"],
            "employment_id": vacancy_data["employment_id"],
            "created_at": vacancy_data["created_at"],
            "level": vacancy_data ["vacancy_level"]
            }
        model_object = get_or_create(Vacancy, **vacancy)
        return model_object

    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}"


class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, unique=True)   
    name =  db.Column(db.String(128), unique=True)   

    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}, employer_name:{self.name}"
