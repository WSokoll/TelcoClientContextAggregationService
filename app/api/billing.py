from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.app import context_db
from flask import Blueprint

bp = Blueprint('billing_api', __name__)


# example of the correct request body:
# {
#     'paymentsHistory': [],
#     'serviceUsage': ''
# }
@bp.route('/set/billing/<int:user_id>', methods=['POST'])
@jwt_required()
def set_billing_data(user_id: int):
    try:
        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']

        if not user:
            return jsonify({'message': 'User with this user_id not found'}), 404

        data = request.json
        payments_history = data.get('paymentsHistory')
        service_usage = data.get('serviceUsage')

        if payments_history is None or service_usage is None:
            return jsonify('Not supported body format'), 400

        user['billingData'] = {
            'paymentsHistory': payments_history,
            'serviceUsage': service_usage
        }

        context_db.db.contexts.update_one({'userId': int(user_id)}, {'$set': user})

    except KeyError:
        return jsonify('Not supported body format'), 400

    return jsonify(user), 200


# examples of the correct request body:
# {
#     "newPaymentsHistory": ["new data"]
# }
# {
#     "serviceUsage": "new service usage"
# }
# {
#     "newPaymentsHistory": ["new data"],
#     "serviceUsage": "new service usage"
# }
@bp.route('/update/billing/<int:user_id>', methods=['PATCH'])
@jwt_required()

def update_billing_data(user_id: int):
    try:
        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']

        if not user:
            return jsonify({'message': 'User with this user_id not found'}), 404

        data = request.json
        new_payments_history = data.get('newPaymentsHistory')
        service_usage = data.get('serviceUsage')

        if new_payments_history is None and service_usage is None:
            return jsonify('Not supported body format'), 400

        if new_payments_history is not None:
            for payment in new_payments_history:
                user['billingData']['paymentsHistory'].append(payment)

        if service_usage is not None:
            user['billingData']['serviceUsage'] = service_usage

        context_db.db.contexts.update_one({'userId': int(user_id)}, {'$set': user})

    except KeyError:
        return jsonify('Not supported body format'), 400

    return jsonify(user), 200
