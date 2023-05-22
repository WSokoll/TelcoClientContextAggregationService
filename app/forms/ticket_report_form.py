from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length


class TicketReportForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired(), Length(max=500)])
    category = SelectField('Problem category', validators=[InputRequired()], choices=[])
