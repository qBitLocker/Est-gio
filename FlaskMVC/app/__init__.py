from flask import Flask 
from mvc_flask import FlaskMVC
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.security.cipher_tools import CipherTools

db = SQLAlchemy()

# run flask run at WebPython/FlaskMVC/
def create_app():
    app = Flask(__name__)
    
    #database = CipherTools(path='app/security/secret', filename='db.bin').AES_dec().decode('utf-8')
    #password = CipherTools(path='app/security/secret', filename='pass.bin').AES_dec().decode('utf-8')
    #username = CipherTools(path='app/security/secret', filename='user.bin').AES_dec().decode('utf-8')

    #app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@192.168.1.60:3306/{database}'

    # flask db init
    # flask db migrate
    # flask db upgrade
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:avance@localhost:3306/test'
    FlaskMVC(app)

    db.init_app(app)
    Migrate(app, db)

    return app