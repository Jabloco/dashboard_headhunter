from app import db

class Vacancy(db.Model):
    id = db.Column(db.Integer(64), primary_key=True)
    hh_id = db.Column(db.Integer(64), unique=True)
    salary_from = db.Column(db.Integer(64))
    salary_to = db.Column(db.Integer(64))
    currency_id = db.Column(db.String(128))
    experience_id = db.Column(db.String(128))
    schedule_id = db.Column(db.String(128))
    employment_id = db.Column(db.String(128))
    area_id = db.Column(db.Integer(64), db.ForeignKey("area.id"))
    employer_id = db.Column(db.Integer(64), db.ForeignKey("employer.id"))
    created_at = db.Column(db.Date(64))
    level = db.Column(db.String(128))
    vacancy_skills = db.relationship("vacancy_skill", backref="vacancy", lazy="dynamic")

    def __repr__(self):
        pass
    
class Employer(db.Model):
    id = db.Column(db.Integer(64), primary_key=True)
    hh_id = db.Column(db.Integer(64), unique=True)   
    name =  db.Column(db.String(128), unique=True)   

    def __repr__(self):
        pass