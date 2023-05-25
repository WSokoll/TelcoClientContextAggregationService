from flask import Blueprint, render_template
from flask_login import current_user
from flask_security import auth_required
from app.app import context_db

bp = Blueprint('tickets', __name__)


@bp.route('/tickets', methods=['GET'])
@auth_required()
def get():

    tickets = context_db.db.contexts.find_one({'userId': current_user.id}).get('tickets', {})

    return render_template('tickets.jinja', tickets=tickets)
