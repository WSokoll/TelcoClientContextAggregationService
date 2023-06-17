from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class TicketReportForm(FlaskForm):
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=500)])
    category = SelectField('Problem category', validators=[InputRequired()], choices=[])
