from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from ..models import Team

teams_collection = db.teams

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """Fetches a team by ID"""
    team_data = teams_collection.find_one({"_id": ObjectId(team_id)})
    if team_data:
        fetched_team = Team(**team_data)
        return jsonify({
            fetched_team
        })
    return abort(404, description="Team not found")