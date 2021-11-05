from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
from webapp.models import Area, KeySkill, Vacancy, Employer
migrate = Migrate(app, db)

from webapp import routes

