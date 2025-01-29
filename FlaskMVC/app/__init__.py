from flask import Flask 
from mvc_flask import FlaskMVC
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.security.cipher_tools import CipherTools

db = SQLAlchemy()

# run flask run at WebPython/FlaskMVC/
def create_app():
    app = Flask(__name__)
    # flask db init
    # flask db migrate
    # flask db upgrade
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{None}:{None}@{None}:{None}/test'
    FlaskMVC(app)

    db.init_app(app)
    Migrate(app, db)

    return app