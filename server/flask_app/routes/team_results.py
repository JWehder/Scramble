from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId
from ..models import TeamResult

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

team_result_bp = Blueprint('team_results', __name__)
