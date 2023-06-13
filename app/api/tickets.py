from flask import jsonify, request, json
from app.app import context_db, mail_service
from flask import Blueprint

bp = Blueprint('tickets_api', __name__)


# this PATCH request body must be like example below:
# {
#     "user_id": 2,
#     "status": "IN-PROGRESS"
# }
@bp.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def patch_change_ticket_status(ticket_id: int):
    content = request.data.decode("utf-8")
    data = json.loads(content)

    try:
        actual_ticket_status = data['status']
        user_id = data['user_id']
        user = context_db.db.contexts.find_one({'userId': int(user_id)})

        del user['_id']

        user_name = user['personalData']['name']
        user_email = user['personalData']['email']

        mail_service.send_ticket_status_changed(user_email, user_name, ticket_id, actual_ticket_status)

    except KeyError:
        return jsonify('Not supported body format'), 400

    return jsonify(actual_ticket_status), 200
