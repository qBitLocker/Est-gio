from flask import Flask
from flask import render_template
from flask import request
from flask_mysqldb import MySQL

from blueprint import blueprint
from dao.cadmer_export_dao import ProductDataAccess
from security.cipher_algo import CipherTools

#app = Flask(__name__)
app = Flask(
    import_name=__name__,
    template_folder='templates',
    static_folder='static'
)

@app.route("/query", methods=['GET', 'POST'])
def query_handler():
    # Processando requisicoes GET
    if request.method == 'GET':
        return render_template('index.html')
    
    # Processando requisicoes POST
    elif request.method == 'POST':
        product_id = request.form['product_id']

        result = dao.get_product_by_id(product_id)

        # Processando os resultados
        if result:
            description, price = result
            return render_template('index.html', description=description, price=price)
        else:
            return render_template('index.html', description=None)

if __name__ == "__main__":
    db   = CipherTools(path='security/secret', filename='db.bin')
    pswd = CipherTools(path='security/secret', filename='pass.bin')
    user = CipherTools(path='security/secret', filename='user.bin')

    app.config['MYSQL_HOST'] = '192.168.1.60'
    app.config['MYSQL_USER'] = user.AES_dec().decode('utf-8')
    app.config['MYSQL_PASSWORD'] = pswd.AES_dec().decode('utf-8')
    app.config['MYSQL_DB'] = db.AES_dec().decode('utf-8')

    # Conexão com o banco de dados
    mysql = MySQL(app)
    #dao = ProductDataAccess(mysql)
    dao = ProductDataAccess(mysql)

    app.run(host='localhost', port=8080)