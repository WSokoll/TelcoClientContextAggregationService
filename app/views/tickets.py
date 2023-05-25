from flask import Blueprint, render_template, flash, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from flask_login import current_user
from flask_security import auth_required
from flask import current_app

bp = Blueprint('tickets', __name__)


@bp.route('/tickets', methods=['GET'])
@auth_required()
def get_tickets():
    context_db = PyMongo()
    context_db.init_app(current_app)

    customer = current_user
    tickets = context_db.db.contexts.find_one({'userId': customer.id}).get('tickets', {})

    return render_template('tickets.jinja', tickets=tickets)