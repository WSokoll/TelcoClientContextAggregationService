from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security, hash_password
from flask_security.models import fsqla_v2


db = SQLAlchemy()
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

    app.config["SECURITY_DATETIME_FACTORY"] = datetime.now
    app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}"
                                             f"@{app.config['DB_HOST']}/{app.config['DB_NAME']}")

    db.init_app(app)

    from sqlalchemy import Column, Integer, ForeignKey
    fsqla_v2.FsModels.db = db
    fsqla_v2.FsModels.user_table_name = "user"
    fsqla_v2.FsModels.role_table_name = "role"
    fsqla_v2.FsModels.roles_users = db.Table(
        "roles_users",
        Column("user_id", Integer(), ForeignKey(f"user.id")),
        Column("role_id", Integer(), ForeignKey(f"role.id")),
        extend_existing=True
    )

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    security.init_app(app, user_datastore)

    @app.before_first_request
    def db_init():
        if not user_datastore.find_role(role='Admin'):
            db.session.add(Role(name='Admin'))
        if not user_datastore.find_role(role='Customer'):
            db.session.add(Role(name='Customer'))
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
        db.session.commit()

    from app.views.home import bp as bp_home
    app.register_blueprint(bp_home)

    return app
