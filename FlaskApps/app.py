from flask import Flask
from flask import render_template
from flask import request

from flask_mysqldb import MySQL

import os
from dotenv import load_dotenv

from blueprint import blueprint
from dao.cadmer_export_dao import ProductDataAccess


#app = Flask(__name__)
app = Flask(
    import_name=__name__,
    template_folder='templates',
    static_folder='static'
)

# Registering the blueprints
app.register_blueprint(blueprint)

# Loading the env variables at .env file
load_dotenv()

# Configuring DataBase Communication
#app.config['MYSQL_HOST'] = '192.168.1.60'
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')

#app.config['MYSQL_USER'] = 'consulta'
app.config['MYSQL_USER'] = os.getenv('DB_USER')

#app.config['MYSQL_PASSWORD'] = 'consulta3722'
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASS')

#app.config['MYSQL_DB'] = 'retguarda'
app.config['MYSQL_DB'] = os.getenv('DB_INTERFACE')

app.extensions['mysql'] = mysql = MySQL(app)
dao = ProductDataAccess()


@app.route("/")
def hello_world():
    return '<h1>Hello, World from Flask</h1>'

# Specify the interface name and the 
@app.route("/form", methods=['GET', 'POST'])
def form_render():
    # Processing GET requests
    if request.method == 'GET':
        return render_template('index.html')
    
    # Processing POST requests
    elif request.method == 'POST':
        product_id = request.form['product_id']

        # Creating a query
        QUERY = '''
            SELECT descricao, app_precovenda as venda 
            FROM cadmer_exportacao
            WHERE codbarra=%s
        '''

        cursor = mysql.connection.cursor()

        # All of the %s MUST be linked with a python tuple
        cursor.execute(QUERY, (product_id,))

        # Taking the fetch results <- return a tuple
        result = cursor.fetchone()
        cursor.close()

        # Processing the results
        if result:
            # print(result)
            description, price = result
            return render_template('index.html', description=description, price=price)
        else:
            return render_template('index.html', description=None)
            # return 'Product not found', 404

@app.route("/form2", methods=['GET', 'POST'])
def form_render():
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
            # return 'Product not found', 404
if __name__ == "__main__":
    app.run(host='localhost', port=8080)