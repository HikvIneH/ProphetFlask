from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    username = db.Column(db.String(15), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #user_file_id = db.Column(db.Integer, db.ForeignKey('user_files.id'))
    user_file = db.relationship('Data', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Data(db.Model):
    __tablename__ = 'user_files'

    id = db.Column(db.Integer, primary_key=True)
    #file_name = db.Column(db.String(60), unique=True)
    name = db.Column(db.String(50), index=True, unique=False)
    data = db.Column(db.LargeBinary)
    #users = db.relationship('User', backref='user_file', lazy='dynamic')
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    #updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<User_File: {}>'.format(self.name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


