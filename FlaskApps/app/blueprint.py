# Blueprints funciona como routes em node.js
# Com este objeto você pode criar rotas em arquivos for de app.py 
# Essas rotas devem ser registradas em app.py
from flask import Blueprint

blueprint = Blueprint("blueprint", __name__)

@blueprint.route("/blueprint")
def blueprint_handler():
    return "<p>This paragraph is a route registered by a blueprint</p>"