from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length


class ProblemReportForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=255)])
    description = StringField('Description', validators=[InputRequired(), Length(max=500)])
    category = SelectField('Problem category', validators=[InputRequired()], choices=[])
