from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

hh_app = Flask(__name__)
hh_app.config.from_object(Config)
db = SQLAlchemy(hh_app)
from app.models import Area, KeySkill, Vacancy, Employer
migrate = Migrate(hh_app, db)

from app import routes

