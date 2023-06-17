from flask import Blueprint, render_template
from app.app import context_db

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def get():
    services = context_db.db.services.find()
    all_healthy = True
    for service in services:
        del service['_id']
        if service['status'] == 'unhealthy' or service['status'] == 'down':
            all_healthy = False
            break
    services = context_db.db.services.find()
    return render_template('home.jinja', services=services, all_healthy=all_healthy)
