from flask import jsonify, abort
from . import leagues_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId
from model import Team

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

teams_collection = db.teams
leagues_collection = db.leagues

@leagues_bp.route('/leagues/<league_id>', methods=['GET'])
def get_teams_by_league_id(league_id):
    """Fetches a round by ID"""
    league = leagues_collection.find_one({"_id": ObjectId(league_id)})
    if league:
        
        return jsonify({
            teams_data
        })
        return abort(404, description="Teams not found for this league.")
    else:
        return abort(404, description="League not found")