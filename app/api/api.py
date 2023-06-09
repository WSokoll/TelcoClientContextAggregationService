from flask import jsonify, request, json
from app.app import context_db
from app.email.email_service import MailService
from flask import Blueprint

bp = Blueprint('api', __name__)
m = MailService()


@bp.route('/api/users/<user_id>', methods=['GET'])
# Method to handle whole context obtainment by user_id
def get_user_by_id(user_id):
    try:
        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']
        return jsonify(user), 200
    except ValueError:
        return jsonify('Parameter user_id must be an integer'), 400


@bp.route('/api/users', methods=['GET'])
@bp.route('/api/users/', methods=['GET'])
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


@bp.route('/api/tickets/<ticket_id>', methods=['PATCH'])
def patch_change_ticket_status(ticket_id):
    content = request.data.decode("utf-8")
    data = json.loads(content)
    try:
        actual_ticket_status = data["status"]
        m.send_ticket_status_changed("syrnikkonrad@gmail.com", "Konrad", ticket_id, actual_ticket_status)
    except KeyError:
        return jsonify("Not supported body format"), 400
    return jsonify(actual_ticket_status), 200


# TODO
# 1. Endpoint for setting up and revoking information about global failure
# 2. Endpoint for changing the ticket status as well as setting up resolution information/guidence for a specific ticket (api/ticket/<ticket_id>
# 3. Endpoint for setting up and patching information about billingData
# 4. Endpoint for patching technicalData
# 5. Endpoint for setting up and patching information about crmData
# 6. Endpoint for user registration with only user_id, personalData and empty tickets