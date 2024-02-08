from flask import request, session, jsonify, send_file, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import traceback
from functools import wraps
from config import app, db, api
from config import Flask, SQLAlchemy, db

#HTTP Constants 
HTTP_SUCCESS = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_CONFLICT = 409
HTTP_SERVER_ERROR = 500
HTTP_UNPROCESSABLE_ENTITY = 422

@app.route('/', methods=['GET'])
def hello_world():
    return {"routes": "working!"}

@app.route('/dummy', methods=['GET'])
def dummy():
    import json
    with open('./results/test.json') as f:
        data = json.load(f)
    response = make_response(
        data,
        200
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/tournaments', methods=['GET'])
def get_tournaments():
    import json
    with open('./results/test.json') as f:
        data = json.load(f)
    response = make_response(
        data,
        200
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/sets/<int:id>', methods=['GET', 'POST', 'DELETE'])
def modify_sets(set_id):
    if request.method == 'GET':
        # retrieve the terms by the particular set that was selected
        # _set = Set.query.filter_by(id=set_id).first()
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)

