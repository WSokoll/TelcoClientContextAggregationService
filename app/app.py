from datetime import datetime

from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security, hash_password
from flask_security.models import fsqla_v2

# MySQL
app_db = SQLAlchemy()

# MongoDB
context_db = PyMongo()

security = Security()


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        static_url_path='/static'
    )

    app.config.from_pyfile('config.default.py')
    app.config.from_pyfile('../local/config.local.py')

    # MongoDB connection and setup
    if app.config['MONGODB_AUTH_ENABLED']:
        app.config["MONGO_URI"] = (
            f"mongodb://{app.config['MONGODB_USER']}:{app.config['MONGODB_PASSWORD']}@{app.config['MONGODB_HOST']}:"
            f"{app.config['MONGODB_PORT']}/{app.config['MONGODB_DB_NAME']}")
    else:
        app.config["MONGO_URI"] = (
            f"mongodb://{app.config['MONGODB_HOST']}:{app.config['MONGODB_PORT']}/{app.config['MONGODB_DB_NAME']}")

    context_db.init_app(app)


    # MySQL and Security setup
    app.config["SECURITY_DATETIME_FACTORY"] = datetime.now
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}"
        f"@{app.config['MYSQL_HOST']}:{app.config['MYSQL_PORT']}/{app.config['MYSQL_DB_NAME']}")

    app_db.init_app(app)

    with app.app_context():
        app_db.reflect()

    from sqlalchemy import Column, Integer, ForeignKey
    fsqla_v2.FsModels.db = app_db
    fsqla_v2.FsModels.user_table_name = "user"
    fsqla_v2.FsModels.role_table_name = "role"
    fsqla_v2.FsModels.roles_users = app_db.Table(
        "roles_users",
        Column("user_id", Integer(), ForeignKey(f"user.id")),
        Column("role_id", Integer(), ForeignKey(f"role.id")),
        extend_existing=True
    )

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(app_db, User, Role)

    security.init_app(app, user_datastore)

    @app.before_first_request
    def db_init():
        # init app database
        if not user_datastore.find_role(role='Admin'):
            app_db.session.add(Role(name='Admin'))
        if not user_datastore.find_role(role='Customer'):
            app_db.session.add(Role(name='Customer'))
        if not user_datastore.find_user(email=app.config['ADMIN_EMAIL']):
            user_datastore.create_user(
                email=app.config['ADMIN_EMAIL'],
                password=hash_password(app.config['ADMIN_PASSWORD']),
                confirmed_at=datetime.now(),
                roles=['Admin']
            )
        if not user_datastore.find_user(email=app.config['CUSTOMER_EMAIL']):
            user_datastore.create_user(
                email=app.config['CUSTOMER_EMAIL'],
                password=hash_password(app.config['CUSTOMER_PASSWORD']),
                confirmed_at=datetime.now(),
                roles=['Customer']
            )
        app_db.session.commit()

        # init context database
        customer = user_datastore.find_user(email=app.config['CUSTOMER_EMAIL'])

        if not context_db.db.contexts.count_documents({'userId': customer.id}):
            context_db.db.contexts.insert_one({
                'userId': customer.id,
                'personalData': {
                    'email': app.config['CUSTOMER_EMAIL'],
                    'name': 'Adam',
                    'surname': 'Kowalski',
                    'age': 30,
                    'gender': 'male',
                    'city': 'Cracow',
                    'state': 'Poland'
                },
                'technicalData': {
                    'modemRouterBrand': 'Netgear',
                    'modemRouterModel': 'Nighthawk M5 MR5200',
                    'mobilePhoneBrand': 'Nokia',
                    'mobilePhoneModel': '3310'
                },
                'crmData': {
                    'subscriptionType': 'monthly subscription'
                },
                'billingData': {
                    'paymentsHistory': [],
                    'serviceUsage': ''
                },
                'tickets': {}
            })

        if not context_db.db.services.count_documents({'serviceName': 'GSM Network'}):
            context_db.db.services.insert_one({
                'serviceName': 'GSM Network',
                'status': 'healthy',
                'impactedLocations': []
            })
        if not context_db.db.services.count_documents({'serviceName': '3G Network'}):
            context_db.db.services.insert_one({
                'serviceName': '3G Network',
                'status': 'unhealthy',
                'impactedLocations': ['Cracow', 'Katowice']
            })
        if not context_db.db.services.count_documents({'serviceName': 'EDGE Network'}):
            context_db.db.services.insert_one({
                'serviceName': 'EDGE Network',
                'status': 'healthy',
                'impactedLocations': []
            })
        if not context_db.db.services.count_documents({'serviceName': 'LTE Network'}):
            context_db.db.services.insert_one({
                'serviceName': 'LTE Network',
                'status': 'down',
                'impactedLocations': ['Gdansk', 'Warsaw', 'Zakopane', 'Cracow']
            })
        if not context_db.db.services.count_documents({'serviceName': '5G Network'}):
            context_db.db.services.insert_one({
                'serviceName': '5G Network',
                'status': 'healthy',
                'impactedLocations': []
            })
        if not context_db.db.services.count_documents({'serviceName': 'Chat Service'}):
            context_db.db.services.insert_one({
                'serviceName': 'Chat Service',
                'status': 'healthy',
                'impactedLocations': []
            })

    from app.views.home import bp as bp_home
    app.register_blueprint(bp_home)

    from app.views.report import bp as bp_report
    app.register_blueprint(bp_report)

    from app.views.tickets import bp as bp_tickets
    app.register_blueprint(bp_tickets)

    from app.api.api import bp as bp_api
    app.register_blueprint(bp_api)

    return app
