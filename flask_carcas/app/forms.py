from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    vacancy_name = StringField("Введи вакансию", validators=[DataRequired()])
    submit = SubmitField("Искать")