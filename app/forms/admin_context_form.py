from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class AdminContextForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=80)])
    surname = StringField('Surname', validators=[InputRequired(), Length(max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(max=80)])
    country = SelectField('Country', validators=[InputRequired()], choices=[])
    city = SelectField('City', validators=[InputRequired()], choices=[])
    router = SelectField('Router', validators=[InputRequired()], choices=[])
    status = SelectField('Status', validators=[InputRequired()], choices=[])