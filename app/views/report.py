from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from flask_security import auth_required
from wtforms import TextAreaField

from app.app import context_db
from app.forms.ticket_report_form import TicketReportForm

bp = Blueprint('report', __name__)


PROBLEM_CATEGORIES = ['Connectivity problems', 'Hardware issues', 'Billing issues', 'Service interruptions',
                      'Security concerns', 'General usability issues', 'Other']


@bp.route('/report', methods=['GET', 'POST'])
@auth_required()
def get_post():

    form = TicketReportForm()
    form.category.choices = PROBLEM_CATEGORIES

    if form.validate_on_submit():

        ticket = {
            'issueType': form.category.data,
            'issueDescription': form.description.data,
            'status': 'reported'
        }

        # save ticket to the context database
        context_db.db.contexts.update_one(
            {'userId': current_user.id},
            {'$set': {'tickets.' + str(current_user.id) + datetime.now().strftime('%H%M%S%d%m%y'): ticket}}
        )

        flash('Problem has been reported')
        return redirect(url_for('home.get'))

    return render_template('report.jinja', form=form)
