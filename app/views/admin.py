from flask import Blueprint, render_template, flash, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from flask_login import current_user
from flask_security import auth_required
from flask import current_app
from app.app import context_db
from app.api.users import get_all_users
from app.forms.admin_context_form import AdminContextForm

bp = Blueprint('admin', __name__)

@bp.route('/admin', methods=['GET', 'POST'])
@auth_required()
def get_context():
   form = AdminContextForm()
   users = get_all_users()[0]
    
   return render_template('admin.jinja', form=form, users=users)