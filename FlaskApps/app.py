from flask import Flask
from flask import render_template
from flask import request

from flask_mysqldb import MySQL

import os
from dotenv import load_dotenv

from blueprint import blueprint
from dao.cadmer_export_dao import ProductDataAccess
from security.cipher_algo import CipherTools

#app = Flask(__name__)
app = Flask(
    import_name=__name__,
    template_folder='templates',
    static_folder='static'
)


@app.route("/")
def hello_handler():
    return '<h1>Hello, World from Flask</h1>'

@app.route("/query", methods=['GET', 'POST'])
def query_handler():
    # Processing GET requests
    if request.method == 'GET':
        return render_template('index.html')
    
    # Processing POST requests
    elif request.method == 'POST':
        product_id = request.form['product_id']

        result = dao.get_product_by_id(product_id)

        # Processing the results
        if result:
            # print(result)
            description, price = result
            return render_template('index.html', description=description, price=price)
        else:
            return render_template('index.html', description=None)
        
if __name__ == "__main__":
    # Registering the blueprints
    app.register_blueprint(blueprint)

    # Loading the env variables at .env file
    load_dotenv()

    # Configuring DataBase Communication
    #app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
    ip = CipherTools(path='security/secret', filename='ip.bin')
    db = CipherTools(path='security/secret', filename='db.bin')
    pswd = CipherTools(path='security/secret', filename='pass.bin')
    user = CipherTools(path='security/secret', filename='user.bin')

    app.config['MYSQL_HOST'] = ip.AES_dec()
    app.config['MYSQL_USER'] = user.AES_dec()
    app.config['MYSQL_PASSWORD'] = pswd.AES_dec()
    app.config['MYSQL_DB'] = db.AES_dec()

    app.extensions['mysql'] = mysql = MySQL(app)

    # Instantiate the Product Data Acess with app context like this
    with app.app_context():
        dao = ProductDataAccess()

    app.run(host='localhost', port=8080)