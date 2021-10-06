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
    id = db.Column(db.Integer(64), primary_key=True)
    hh_id = db.Column(db.Integer(64), unique=True, nullable=False)
    salary_from = db.Column(db.Integer(64))
    salary_to = db.Column(db.Integer(64))
    currency_id = db.Column(db.String(128))
    experience_id = db.Column(db.String(128))
    schedule_id = db.Column(db.String(128))
    employment_id = db.Column(db.String(128))
    area_id = db.Column(db.Integer(64), db.ForeignKey("area.id"),nullable=False)
    employer_id = db.Column(db.Integer(64), db.ForeignKey("employer.id"),nullable=False) 
    created_at = db.Column(db.Date(64), nullable=False)
    level = db.Column(db.String(128), nullable=False)
    area = db.relationship("Area", backref="vacancies")
    employer = db.relationship("Employer", backref="vacancies")

    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}"


class Employer(db.Model):
    id = db.Column(db.Integer(64), primary_key=True)
    hh_id = db.Column(db.Integer(64), unique=True)   
    name =  db.Column(db.String(128), unique=True)   

    def __repr__(self):
        return f"id:{self.id}, hh_id:{self.hh_id}, employer_name:{self.name}"
