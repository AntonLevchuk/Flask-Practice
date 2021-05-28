from flask import Flask, request, redirect, url_for
from config import Configuration

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


from flask_login import current_user

from flask_security import Security, SQLAlchemyUserDatastore

from models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)
    db.init_app(app)
    return app


app = create_app()
app.app_context().push()

db.create_all()


# flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# admin user
user_datastore.create_user(email='admin4@local.com', password='admin')
user = User.query.first()

user_datastore.create_role(name='admin', description='administrator')

role = Role.query.first()
user_datastore.add_role_to_user(user, role)

# ADMIN


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


admin = Admin(app, 'FlaskApp', url='/admin', index_view=HomeAdminView(name='Home'))
admin.add_view(AdminView(Author, db.session))
admin.add_view(AdminView(Book, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
