class Configuration(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://userr:password@localhost/flaskdata'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = "webapp"
    DEBUG = True


# Flask-Security
    SECRET_KEY = 'mysecret'
    SECURITY_PASSWORD_SALT = 'mysecretsalt'
    SECURITY_REGISTERABLE = True
