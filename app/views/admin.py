from flask import Blueprint, render_template, flash, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from flask_login import current_user
from flask_security import auth_required
from flask import current_app
from app.app import context_db

bp = Blueprint('admin', __name__)


@bp.route('/admin', methods=['GET'])
@auth_required()
def index():

    return render_template('admin.jinja')