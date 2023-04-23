from app.app import db
from flask_security.models import fsqla_v2


class Role(db.Model, fsqla_v2.FsRoleMixin):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return self.name


class User(db.Model, fsqla_v2.FsUserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return self.email

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]


class Problems(db.Model):
    __tablename__ = 'problems'
    __table_args__ = {'extend_existing': True}
