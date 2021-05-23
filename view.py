from app import *

from flask import render_template
from flask import request

from flask_security.utils import hash_password


@app.route('/')
def index():
    return render_template('index.html')


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