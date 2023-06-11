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


# this PATCH request body must be like example below:
# {
#     "user_id": 2,
#     "status": "IN-PROGRESS"
# }
@bp.route('/api/tickets/<ticket_id>', methods=['PATCH'])
def patch_change_ticket_status(ticket_id):
    content = request.data.decode("utf-8")
    data = json.loads(content)
    try:
        actual_ticket_status = data['status']
        user_id = data['user_id']
        user = context_db.db.contexts.find_one({'userId': int(user_id)})
        del user['_id']
        user_name = user['personalData']['name']
        user_email = user['personalData']['email']
        # m.send_ticket_status_changed(user_email, user_name, ticket_id, actual_ticket_status)

        # for testing only
        # m.send_ticket_status_changed('syrnikkonrad@gmail.com', 'Konrad', ticket_id, actual_ticket_status)
    except KeyError:
        return jsonify('Not supported body format'), 400
    return jsonify(actual_ticket_status), 200


@bp.route('/api/services/<serviceName>', methods=['GET'])
def get_service_by_serviceName(serviceName):
    try:
        service = context_db.db.services.find_one({'serviceName': serviceName})
        del service['_id']
        return jsonify(service), 200
    except ValueError:
        return jsonify('Parameter serviceName is incorrect'), 400


@bp.route('/api/services', methods=['GET'])
def get_service_by_parameters():
    args = request.args
    params = dict()
    if not bool(args):
        return jsonify('Query parameter must be passed'), 400
    for key, value in args.items():
        if key not in ['serviceName', 'status', 'impactedLocations']:
            return jsonify('Unsupported query parameter: ' + key), 400
        params[key] = value
    output = []
    services = context_db.db.services.find(params)
    for service in services:
        service_data = dict()
        service_data['serviceName'] = service['serviceName']
        service_data['status'] = service['status']
        service_data['impactedLocations'] = service['impactedLocations']
        output.append(service_data)
    return jsonify(output), 200


@bp.route('/api/services/<serviceName>', methods=['POST'])
def update_service_by_serviceName(serviceName):
    try:
        service = context_db.db.services.find_one({'serviceName': serviceName})
        if not service:
            return jsonify('Service not found'), 404

        data = request.json
        new_status = data.get('newStatus')
        impacted_locations = data.get('impactedLocations')

        if impacted_locations:
            service['impactedLocations'] = impacted_locations
        if new_status:
            service['status'] = new_status
            if new_status == 'healthy':
                impacted_locations = []
                service['impactedLocations'] = impacted_locations

        context_db.db.services.update_one({'serviceName': serviceName}, {'$set': service})
        del service['_id']
        return jsonify(service), 200
    except Exception as e:
        return jsonify(str(e)), 400

# TODO
# 1. Endpoint for setting up and revoking information about global failure
# 2. Endpoint for changing the ticket status as well as setting up resolution information/guidence for a specific ticket (api/ticket/<ticket_id>
# 3. Endpoint for setting up and patching information about billingData
# 4. Endpoint for patching technicalData
# 5. Endpoint for setting up and patching information about crmData
# 6. Endpoint for user registration with only user_id, personalData and empty tickets
