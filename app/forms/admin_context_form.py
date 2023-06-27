from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class AdminContextForm(FlaskForm):
    user_id = StringField('ID', validators=[Length(max=80)])
    name = StringField('Name', validators=[Length(max=80)])
    surname = StringField('Surname', validators=[Length(max=80)])
    email = StringField('Email', validators=[Length(max=80)])
    age = StringField('Age', validators=[Length(max=80)])
    gender = SelectField('Gender', choices=[])
    state = SelectField('State', choices=[])
    city = SelectField('City', choices=[])
    router_brand = SelectField('Router brand', choices=[])
    router_model = SelectField('Router model', choices=[])
    mobile_brand = SelectField('Mobile brand', choices=[])
    mobile_model = SelectField('Mobile model', choices=[])
    subscription_type = SelectField('Subscription type', choices=[])