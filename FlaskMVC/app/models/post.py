from app import db

# Classe que extende um model database
class Post(db.Model):
    # Criando uma tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)