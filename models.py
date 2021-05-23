from flask_security import UserMixin, RoleMixin

from flask_sqlalchemy import SQLAlchemy
'''
try:
    from app import app as app
except ImportError:
    from __main__ import app
'''
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    birthday = db.Column(db.Date)
    name = db.Column(db.String(32), unique=True)

    def __init__(self, id, birthday, name):
        self.id = id
        self.name = name
        self.birthday = birthday

    def __repr__(self, *args, **kwargs):
        return f'{self.id}.{self.name}'


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    published = db.Column(db.Float)
    is_published = db.Column(db.Boolean, default=True)

    def __init__(self, id, title, published, is_published):
        self.id = id
        self.title = title
        self.published = published
        self.is_published = is_published

    def __repr__(self, *args, **kwargs):
        return f'{self.id}.{self.title}'

    book_name = db.Column(db.String(32), db.ForeignKey('author.name'))
    name = db.relationship('Author', backref=db.backref('book', lazy=True))


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))