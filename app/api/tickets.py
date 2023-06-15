from flask import jsonify, request, json
from app.app import context_db, mail_service
from flask import Blueprint

bp = Blueprint('tickets_api', __name__)


# this PATCH request body must be like example below:
# {
#     "user_id": 2,
#     "status": "in-progress"
#     (optional) "feedback": "Please try to restart your device"
# }
@bp.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def patch_change_ticket_status(ticket_id: int):
    try:
        data = request.json
        user_id = data.get('user_id')
        status = data.get('status')
        feedback = data.get('feedback')

        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']

        user_name = user['personalData']['name']
        user_email = user['personalData']['email']

        user['tickets'][str(ticket_id)]['status'] = status
        user['tickets'][str(ticket_id)]['feedback'] = feedback
        if feedback:
            user['tickets'][str(ticket_id)]['feedback'] = feedback
        else:
            user['tickets'][str(ticket_id)].pop('feedback', None)

        context_db.db.contexts.update_one({'userId': int(user_id)}, {'$set': user})

        mail_service.send_ticket_status_changed(user_email, user_name, ticket_id, status, feedback)

    except KeyError:
        return jsonify('Not supported body format'), 400

    return jsonify(user['tickets'][str(ticket_id)]), 200
