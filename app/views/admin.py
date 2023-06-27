from flask import Blueprint, render_template, flash, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from flask_login import current_user
from flask_security import auth_required
from flask import current_app
from app.app import context_db
from app.api.users import get_all_users, get_specified_users
from app.forms.admin_context_form import AdminContextForm

bp = Blueprint('admin', __name__)

def get_choices(users, dataType, data):
   choices = []
   for user in users:
      choices.append(user[dataType][data])
   
   return choices

def fill_form_with_choices(form, users):
   gender_choices = get_choices(users, 'personalData', 'gender')
   state_choices = get_choices(users, 'personalData', 'state')
   city_choices = get_choices(users, 'personalData', 'city')
   router_brand_choices = get_choices(users, 'technicalData', 'modemRouterBrand')
   router_model_choices = get_choices(users, 'technicalData', 'modemRouterModel')
   mobile_brand_choices = get_choices(users, 'technicalData', 'mobilePhoneBrand')
   mobile_model_choices = get_choices(users, 'technicalData', 'mobilePhoneModel')
   subscription_type_choices = get_choices(users, 'crmData', 'subscriptionType')

   form.state.choices = state_choices
   form.city.choices = city_choices
   form.gender.choices = gender_choices
   form.router_brand.choices = router_brand_choices
   form.router_model.choices = router_model_choices
   form.mobile_brand.choices = mobile_brand_choices
   form.mobile_model.choices = mobile_model_choices
   form.subscription_type.choices = subscription_type_choices
   return

@bp.route('/admin', methods=['GET'])
@auth_required()
def get_context():
   form = AdminContextForm()
   all_users = get_all_users()[0]
   
   fill_form_with_choices(form, all_users)

   return render_template('admin.jinja', form=form, users=all_users)

@bp.route('/admin', methods=['POST'])
@auth_required()
def filter_users():
   form = AdminContextForm()

   user_id = form.user_id.data
   email = form.email.data
   name = form.name.data
   surname = form.surname.data
   age = form.age.data
   gender = form.gender.data
   state = form.state.data
   city = form.city.data
   router_brand = form.router_brand.data
   router_model = form.router_model.data
   mobile_brand = form.mobile_brand.data
   mobile_model = form.mobile_model.data
   subscription_type = form.subscription_type.data

   search_criteria = [
      { "personalData.email": email },
      { "personalData.name": name },
      { "personalData.surname": surname },
      { "personalData.age": age },
      { "personalData.gender": gender },
      { "personalData.city": city },
      { "personalData.state": state },
      { "technicalData.modemRouterBrand": router_brand },
      { "technicalData.modemRouterModel": router_model },
      { "technicalData.mobilePhoneBrand": mobile_brand },
      { "technicalData.mobilePhoneModel": mobile_model },
      { "crmData.subscriptionType": subscription_type }
   ]

   query = {}
   for criteria in search_criteria:
      for key, value in criteria.items():
         if value:
            query[key] = value

   users = get_specified_users(query)[0]
   all_users = get_all_users()[0]
   fill_form_with_choices(form, all_users)

   return render_template('admin.jinja', form=form, users=users)
   