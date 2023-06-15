from flask import jsonify, request

from app.app import context_db
from flask import Blueprint

bp = Blueprint('crm_api', __name__)


# example of the correct request body:
# {
#     'subscriptionType': 'monthly subscription'
# }
@bp.route('/set/crm/<int:user_id>', methods=['POST'])
def set_crm_data(user_id: int):
    try:
        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']

        if not user:
            return jsonify({'message': 'User with this user_id not found'}), 404

        data = request.json
        subscription_type = data.get('subscriptionType')

        if subscription_type is None:
            return jsonify('Not supported body format'), 400

        user['crmData'] = {
            'subscriptionType': subscription_type,
        }

        context_db.db.contexts.update_one({'userId': int(user_id)}, {'$set': user})

    except KeyError:
        return jsonify('Not supported body format'), 400

    return jsonify(user), 200
