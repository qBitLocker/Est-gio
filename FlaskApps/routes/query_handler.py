from flask import Blueprint, request

query = Blueprint("query_handler", __name__)

@query.route("/query2", methods=['GET', 'POST'])
def query_handler2():
    if request.method == "GET":
        print ("[Query Handler]: Processing GET")
        return '<h1>Hello, Route GET</h1>'
    elif request.method == "POST":
        print ("[Query Handler]: Processing POST")
        return '<h1>Hello, Route POST</h1>'