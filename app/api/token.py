from flask import Blueprint, request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_security import SQLAlchemyUserDatastore, verify_password
from app.app import app_db


bp = Blueprint('token_api', __name__)

@bp.route('/token', methods=['POST'])
def generate_token():
    email = request.form.get('email')
    password = request.form.get('password')

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(app_db, User, Role)

    if not user_datastore.find_user(email=email) or not verify_password(password, user_datastore.find_user(email=email).password):
        return jsonify({'message': 'Nieprawidlowy login lub haslo'}), 401

    
    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token}), 200


#@bp.route('/protected', methods=['GET'])
#@jwt_required()  # Middleware sprawdzający ważność tokena
#def protected_endpoint():
#   current_user = get_jwt_identity()
#   return jsonify({'message': f'Uzytkownik {current_user} ma dostep do chronionego zasobu'}), 200
