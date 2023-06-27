from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, json
from flask_login import current_user
from flask_security import auth_required
import requests

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
        call_ticket_app_submit_alert()

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


@bp.route('/call_ticket_app/get_token', methods=['POST'])
def call_ticket_app_get_token():
    url = 'http://localhost:8000/api/token/'

    # username = ADMIN_EMAIL
    # password = ADMIN_PASSWORD
    username = 'dupa'
    password = 'Q@wertyuiop'

    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    data2 = json.loads(response.content)
    token = data2["access"]

    return token


@bp.route('/call_ticket_app/submit_alert', methods=['GET'])
def call_ticket_app_submit_alert():
    form = TicketReportForm()

    url = 'http://localhost:8000/api/submit_alert/'
    headers = {
        'Authorization': 'Bearer ' + call_ticket_app_get_token(),
        'Content-Type': 'application/json'
    }
    data = {
        "api_id": str(current_user.id) + datetime.now().strftime('%H%M%S%d%m%y'),
        "reporting_person_id": current_user.id,
        "assigned_person_id": 4,
        "problem_object_id": 4,
        "user_problem_description": form.description.data,
        "problem_description": form.category.data,
        "instalator_report": "Example installer report",
        "priority": 1,
        "status": "New",
        "reporting_time": str(datetime.now()),
        "is_done": False
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.content)

    return response
