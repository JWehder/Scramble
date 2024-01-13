from flask import request, session, jsonify, send_file, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import traceback
from functools import wraps
from config import app, db, api
from models import Set, Flashcard
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

@app.route('/sets/<int:id>', methods=['GET', 'POST', 'DELETE'])
def modify_sets(set_id):
    if request.method == 'GET':
        # retrieve the terms by the particular set that was selected
        _set = Set.query.filter_by(id=set_id).first()
        if _set is None:
            return {'error': 'set not found'}, HTTP_NOT_FOUND
        
        return _set.to_dict(), HTTP_SUCCESS
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass