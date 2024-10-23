from flask import jsonify, abort
from . import teams_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId
from .model import Period

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

teams_collection = db.teams

@teams_bp.route('/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """Fetches a team by ID"""
    pass