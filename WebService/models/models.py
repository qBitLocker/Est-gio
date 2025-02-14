'''
@Author: Vinícius Mari Marrafon
@Date: 2025-02-14

@Description: Para a criação de um Model devemos conhecer exatamente
quais campos a tabela possui, inclusive seus nomes e tipagem. Os Mo-
del são completamente fieis as tabelas do banco de dados;
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class Product (db.Model):
    # Nome da tabela: Se não especificado, será considerado o nome da classe
    __tablename__ = 'cadmer_exportacao'
    # Campos da tabela, junto com seus respectivos tipos e propriedades
    codbarra: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    app_precoVenda: Mapped[float] = mapped_column(db.Float, nullable=False)

class Client (db.Model):
    __tablename__ = 'clientes'
    codigo: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nome:   Mapped[str] = mapped_column(db.String(255), nullable=False)     
