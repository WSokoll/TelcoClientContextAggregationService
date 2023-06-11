from flask import Blueprint, render_template
from app.app import context_db

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def get():

    services = context_db.db.services.find()
    print(services)
    return render_template('home.jinja', services=services)
