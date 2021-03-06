import logging
from os import name

import sqlalchemy.orm.exc

from webapp import db


logging.basicConfig(handlers=[logging.FileHandler('error.log', 'a', 'utf-8')],
                    format='%(levelname)s - %(message)s')

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
    if model_object:
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


def keyskill_vacancy(vacancy, keyskills):
    skills = [KeySkill.insert(skill) for skill in keyskills]
    for skill in skills:
        vacancy.keyskill.append(skill)
        db.session.add(vacancy)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as error:
        logging.exception(error)
        return


class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    @classmethod
    def insert(cls, area_id, area_name):
        """Записывает данные в таблицу Area."""
        model_object, model_exist = get_or_create(cls, hh_id=area_id, name=area_name)
        return model_object

    def __repr__(self):
        return f'id: {self.id}, hh_id: {self.hh_id}, area_name: {self.name}'


class KeySkill(db.Model):
    __tablename__ = 'keyskill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    @classmethod
    def insert(cls, key_skill):
        """Записывает данные в таблицу KeySkill."""
        model_object, model_exist = get_or_create(cls, name=key_skill)
        return model_object

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
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=True)
    created_at = db.Column(db.Date, nullable=False)
    level = db.Column(db.String(128), nullable=False)
    area = db.relationship('Area', backref='vacancies')
    employer = db.relationship('Employer', backref='vacancies')
    keyskill = db.relationship('KeySkill', secondary=vacancy_skill)

    @classmethod
    def insert(
        cls,
        hh_id,
        salary_from,
        salary_to,
        currency_id,
        experience_id,
        schedule_id,
        employment_id,
        area_id,
        employer_id,
        created_at,
        level
        ):
        """Записывает данные в таблицу Vacancy."""
        model_object, _ = get_or_create(
            cls,
            hh_id=hh_id,
            salary_from=salary_from,
            salary_to=salary_to,
            currency_id=currency_id,
            experience_id=experience_id,
            schedule_id=schedule_id,
            employment_id=employment_id,
            area_id=area_id,
            employer_id=employer_id,
            created_at=created_at,
            level=level
            )
        return model_object

    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}"


class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, unique=True, nullable=True)
    name = db.Column(db.String(128))

    @classmethod
    def insert(cls, hh_id, name):
        row, _ = get_or_create(cls, hh_id=hh_id, name=name)
        return row

    def __repr__(self):
        return f"id: {self.id}, hh_id: {self.hh_id}, employer_name: {self.name}"
