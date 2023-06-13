import random
import string
from datetime import datetime

from flask import jsonify, request, abort
from flask_security import SQLAlchemyUserDatastore

from app.app import context_db, app_db, mail_service
from flask import Blueprint

from app.models import User, Role

bp = Blueprint('api', __name__)


@bp.route('/users/<int:user_id>', methods=['GET'])
# Method to handle whole context obtainment by user_id
def get_user_by_id(user_id: int):
    try:
        user = context_db.db.contexts.find_one({'userId': user_id})

        del user['_id']
        return jsonify(user), 200
    except ValueError:
        return jsonify('Parameter user_id must be an integer'), 400


@bp.route('/users', methods=['GET'])
# Can be used to obtain full personalData and userId by parameters
def get_user_by_parameters():
    args = request.args
    params = dict()

    if not bool(args):
        return jsonify('Query parameter must be passed'), 400

    for key, value in args.items():
        if key not in ['name', 'surname', 'email', 'city', 'state']:
            return jsonify('Unsupported query parameter: ' + key), 400

        params["personalData." + key] = value

    output = []
    users = context_db.db.contexts.find(params)

    for user in users:
        user_data = dict()
        user_data['userId'] = user['userId']
        user_data['personalData'] = user['personalData']
        output.append(user_data)

    return jsonify(output), 200


@bp.route('users/register', methods=['POST'])
def register_new_user():
    data = request.get_json()

    required_keys = ['email', 'name', 'surname', 'age', 'gender', 'city', 'state']

    for k in required_keys:
        if k not in data.keys():
            return jsonify(f'{k} required'), 400

    user_datastore = SQLAlchemyUserDatastore(app_db, User, Role)

    if user_datastore.find_user(email=data['email']):
        return jsonify('User with given email already exists'), 400

    # Generate temporal password
    chars = string.ascii_letters + '1234567890' + '!#$%^&*'
    temporal_password = ''.join(random.choice(chars) for i in range(8))

    # Add user to the mySQL database
    user_datastore.create_user(
        email=data['email'],
        password=temporal_password,
        confirmed_at=datetime.now(),
        roles=['Customer']
    )
    app_db.session.commit()

    user = user_datastore.find_user(email=data['email'])

    # Add user to the mongoDB database
    context_db.db.contexts.insert_one({
        'userId': user.id,
        'personalData': {
            'email': data['email'],
            'name': data['name'],
            'surname': data['surname'],
            'age': data['age'],
            'gender': data['gender'],
            'city': data['city'],
            'state': data['state']
        },
        'tickets': {}
    })

    # Send an email with temporal credentials
    mail_service.send_credentials(data['email'], temporal_password, data['name'])

    return jsonify('User registered'), 200
