from os import name
from app import db

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hh_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return f'id: {self.id}, hh_id: {self.hh_id}, area_name: {self.name}'

class KeySkill(db.Model):
    pass
    def __repr__(self):
        pass

class Vacancy(db.Model):
    pass
    def __repr__(self):
        pass

class Employer(db.Model):
    pass
    def __repr__(self):
        pass
    