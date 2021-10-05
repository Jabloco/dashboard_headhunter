from os import name
from app import db

vacancy_skill = db.Table('vacancy_skill',
    db.Column('vacancy_id', db.Integer, db.ForeignKey('vacancy.id'), primary_key=True),
    db.Column('keyskill_id', db.Integer, db.ForeignKey('keyskill.id'), primary_key=True)
)


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'id: {self.id}, hh_id: {self.hh_id}, area_name: {self.name}'


class KeySkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    vacancies = db.relationship('Vacancy', secondary=vacancy_skill)

    def __repr__(self):
        return f'id: {self.id}, keyskill_name: {self.name}'


class Vacancy(db.Model):
    pass

    def __repr__(self):
        pass


class Employer(db.Model):
    pass

    def __repr__(self):
        pass
