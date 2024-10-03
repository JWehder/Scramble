from flask import request, make_response, jsonify, requests
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from functools import wraps
from config import app
from config import Flask
from dotenv import load_dotenv

from config import db

# HTTP Constants 
HTTP_SUCCESS = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_CONFLICT = 409
HTTP_SERVER_ERROR = 500
HTTP_UNPROCESSABLE_ENTITY = 422

@app.route('/start_draft', methods=['POST'])
def start_draft():
    # Your logic to start the draft
    user_id = request.json.get('user_id')
    pick_duration = request.json.get('pick_duration')

    # Start the draft timer via WebSocket
    requests.post('http://localhost:5555/start_draft_timer/', json={'user_id': user_id, 'pick_duration': pick_duration})
    return jsonify({'message': 'Draft started and timer initiated'}), 200

@app.route('/end_draft', methods=['POST'])
def end_draft():
    # Your logic to end the draft
    user_id = request.json.get('user_id')

    # Stop the draft timer via WebSocket
    requests.post('http://localhost:5555/stop_draft_timer/', json={'user_id': user_id})
    return jsonify({'message': 'Draft ended and timer stopped'}), 200

@app.route('/', methods=['GET'])
def hello_world():
    return {"routes": "working!"}
    

@app.route('/tournaments', methods=['GET'])
def get_tournaments():
    import json
    with open('../data/tournaments.json') as f:
        data = json.load(f)
    response = make_response(
        data,
        200
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response 

@app.route('/get_facebook_appId', methods=["GET"])
def get_facebook_appId():
    # Authentication: You might use a more secure method here
    # For simplicity, let's assume the request comes from an allowed origin
    if request.referrer and "http://localhost:3000/" in request.referrer:
        import os

        load_dotenv()

        client_id = os.getenv("FACEBOOK_APP_ID")

        return jsonify({"facebook_app_id": client_id}), HTTP_SUCCESS
    else:
        return jsonify({"error": "Unauthorized"}), HTTP_UNAUTHORIZED

@app.route('/me', methods=['GET'])
def auth():
    if request.method == 'GET':
        pass

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        pass

@app.route('/logout', methods=['DELETE'])
def logout():
    if request.method == 'DELETE':
        pass

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        pass

@app.route("/get_client_id", methods=["GET"])
def get_client_id():
    # Authentication: You might use a more secure method here
    # For simplicity, let's assume the request comes from an allowed origin
    if request.referrer and "http://localhost:3000/" in request.referrer:
        import os

        load_dotenv()

        client_id = os.getenv("CLIENT_ID")

        return jsonify({"client_id": client_id}), HTTP_SUCCESS
    else:
        return jsonify({"error": "Unauthorized"}), HTTP_UNAUTHORIZED


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

