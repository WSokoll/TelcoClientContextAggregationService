from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from flask_security import auth_required

from app.app import db
from app.forms.problem_report_form import ProblemReportForm
from app.models import Problems

bp = Blueprint('report', __name__)


PROBLEM_CATEGORIES = ['Connectivity problems', 'Hardware issues', 'Billing issues', 'Service interruptions',
                      'Security concerns', 'General usability issues', 'Other']


@bp.route('/report', methods=['GET', 'POST'])
@auth_required()
def get_post():

    form = ProblemReportForm()
    form.category.choices = PROBLEM_CATEGORIES

    if form.validate_on_submit():
        problem = Problems(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data
        )

        db.session.add(problem)
        db.session.commit()

        flash('Problem has been reported')
        return redirect(url_for('home.get'))

    return render_template('report.jinja', form=form)
