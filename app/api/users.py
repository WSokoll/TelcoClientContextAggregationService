import random
import string
import uuid
from datetime import datetime

from flask import jsonify, request
from flask_security import SQLAlchemyUserDatastore

from app.app import context_db, app_db, mail_service
from flask import Blueprint

from app.models import User, Role

bp = Blueprint('users_api', __name__)


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


# this POST request body must be like example below:
# {
#   "technicalData": [
#     {
#       "brand": "Apple",
#       "model": "iPhone 12",
#       "type": "smartphone"
#     },
#     {
#       "brand": "Samsung",
#       "model": "Galaxy S21",
#       "type": "smartphone"
#     },
#     {
#       "brand": "HP",
#       "model": "Pavilion",
#       "type": "laptop"
#     }
#   ]
# }
@bp.route('/users/<int:user_id>/technical_data', methods=['POST'])
def add_user_technical_data(user_id: int):
    try:
        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']

        if user:

            data = request.json
            technical_data = data.get('technicalData')

            if technical_data:
                for product in technical_data:
                    model = product.get('model')
                    brand = product.get('brand')
                    product_type = product.get('type')

                    if model and brand and product_type:
                        product_id = str(uuid.uuid4())  # Generating unique id for product
                        user['technicalData'].setdefault('products', []).append({
                            '_id': product_id,
                            'model': model,
                            'brand': brand,
                            'type': product_type
                        })

            context_db.db.contexts.update_one({'userId': int(user_id)}, {'$set': user})
        else:
            return jsonify({'message': 'User with this user_id not found'}), 404

    except KeyError:
        return jsonify('Not supported body format'), 400

    return jsonify(user), 200


@bp.route('/users/<int:user_id>/technical_data/<string:product_id>', methods=['DELETE'])
def delete_user_technical_data(user_id: int, product_id: str):
    try:
        user = context_db.db.contexts.find_one({'userId': int(user_id)})

        if user:
            products = user['technicalData'].get('products', [])

            index = next((index for index, p in enumerate(products) if str(p['_id']) == product_id), None)

            if index is not None:
                # Delete from list
                deleted_product = products.pop(index)

                context_db.db.contexts.update_one({'userId': int(user_id)},
                                                  {'$set': {'technicalData.products': products}})

                return jsonify(
                    {'message': 'Product deleted successfully', 'deleted_product': deleted_product}), 200
            else:
                return jsonify({'message': 'Product with this product_id not found'}), 404
        else:
            return jsonify({'message': 'User with this user_id not found'}), 404

    except Exception as e:
        return jsonify({'message': 'An error occurred'}), 500

@bp.route('/all_users', methods=['GET'])
def get_all_users():
    try:
        users = list(context_db.db.contexts.find({}, {'_id': 0}))
        return users, 200
    except ValueError:
        return jsonify('An error occured'), 400

@bp.route('/specified_users', methods=['GET'])
def get_specified_users(query):
    try:
        users = list(context_db.db.contexts.find(query, {'_id': 0}))
        return users, 200
    except ValueError:
        return jsonify('An error occured'), 400
