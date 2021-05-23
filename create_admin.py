from app import db
from app import user_datastore

from models import User, Role


if __name__ == '__main__':
    email = 'admin@admin.ru'
    password = 'admin'

    user_datastore.create_user(email=email, password=password)
    db.session.commit()

    user_datastore.create_role(name='admin', description='administrator')
    db.session.commit()

    admin_user = User.query.filter_by(email=email).first()
    admin_role = Role.query.filter_by(name='admin').first()

    user_datastore.add_role_to_user(admin_user, admin_role)
    db.session.commit()

    print('Admin user created.\nE-mail: {}\nPassword: {}'.format(email, password))