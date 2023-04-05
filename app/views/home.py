from flask import Blueprint, render_template

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def get():
    return render_template('home.jinja')
