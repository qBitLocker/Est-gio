from flask import Blueprint

blueprint = Blueprint("blueprint", __name__)

@blueprint.route("/blueprint")
def blueprint_handler():
    return "<p>This paragraph is a route registered by a blueprint</p>"