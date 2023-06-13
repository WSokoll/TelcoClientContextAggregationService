from flask import jsonify, request
from app.app import context_db
from flask import Blueprint

bp = Blueprint('services_api', __name__)


@bp.route('/services/<string:serviceName>', methods=['GET'])
def get_service_by_service_name(service_name: str):
    try:
        service = context_db.db.services.find_one({'serviceName': service_name})

        del service['_id']
        return jsonify(service), 200
    except ValueError:
        return jsonify('Parameter serviceName is incorrect'), 400


@bp.route('/services', methods=['GET'])
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


@bp.route('/services/<string:serviceName>', methods=['POST'])
def update_service_by_service_name(service_name: str):
    try:
        service = context_db.db.services.find_one({'serviceName': service_name})
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

        context_db.db.services.update_one({'serviceName': service_name}, {'$set': service})

        del service['_id']
        return jsonify(service), 200

    except Exception as e:
        return jsonify(str(e)), 400
