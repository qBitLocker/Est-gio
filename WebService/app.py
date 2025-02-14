'''
@Author: Vinícius Mari Marrafon
@Date: 2025-02-14

@Description: JSON Web Service para consulta em banco
de dados MySQL.
'''
from flask import Flask, request, jsonify
from security.cipher_algo import CipherTools

# ORM (Mapeamento de Objeto-Relacional)
from sqlalchemy.orm import Mapped, mapped_column
from models.models import db, Product, Client

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

db.init_app(app)

# Interface fetch
@app.route("/fetch", methods=['POST'])
def fetch_handler():
    # Lendo os argumentos da requesicao (?{args}={values})
    # key = request.args.get('key')
    data = request.get_json()
    key = data.get("key")

    if key is None:
        return jsonify({'Erro': 'Forneca a Identificacao (ID) do produto'}), 400

    #value = db.get(key)
    result = Product.query.filter_by(codbarra=key).with_entities(Product.descricao, Product.app_precoVenda).first()

    if result is None:
        return jsonify({'Erro': 'Produto nao encontrado'}), 404

    return jsonify({'Descricao': result.descricao, 'Preco': result.app_precoVenda})

if __name__ == '__main__':
    #password = CipherTools(filename='zalike_pass.bin')
    app.run(host='192.168.1.176', port=8080)