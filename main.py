import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_admin.contrib import sqla
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_login import current_user

from flask_security import Security, SQLAlchemyUserDatastore, login_required, UserMixin, RoleMixin
from flask_security.utils import hash_password


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://userr:password@localhost/flaskdata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'
app.config['SECURITY_PASSWORD_SALT'] = 'mysecretsalt'
FLASK_APP = "webapp"
db = SQLAlchemy(app)
db.init_app(app)


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login_user.html', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login_user.html', next=request.url))


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))


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


# flask-security classes below


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


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                os.abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# admin user
user_datastore.create_user(email='admin1@local.com', password='admin')
user = User.query.first()
db.session.commit()
user_datastore.create_role(name='admin', description='administrator')


role = Role.query.first()
user_datastore.add_role_to_user(user, role)


@app.route('/')
@login_required
def index():
    return redirect(url_for('index.index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_datastore.create_user(
            email=request.form.get('email'),
            password=hash_password(request.form.get('password')),
        )

        db.session.commit()

        return redirect(url_for('admin.index'))

    return render_template('register.html')


db.create_all()
admin.add_view(AdminView(Author, db.session))
admin.add_view(AdminView(Book, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

if __name__ == '__main__':
    app.run(debug=True)

app.run()
