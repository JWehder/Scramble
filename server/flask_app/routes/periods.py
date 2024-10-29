from flask import jsonify, abort, Blueprint
from . import teams_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

periods_bp = Blueprint('periods', __name__)
