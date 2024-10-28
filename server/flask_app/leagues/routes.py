from flask import jsonify, abort
from . import leagues_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from . import League

teams_collection = db.teams
leagues_collection = db.leagues

@leagues_bp.route('/leagues/<league_id>', methods=['GET'])
def get_teams_by_league_id(league_id):
    """Fetches a round by ID"""
    league = leagues_collection.find_one({"_id": ObjectId(league_id)})
    if league:
        if len(league["Teams"]) > 1:
            teams = []
            for team_id in league["Teams"]:
                team = teams_collection.find_one({"_id": team_id})
                if team:
                    teams.append(team)
                else:
                    return abort(404, description=f"There was an error collecting the teams for this league. Team id: {team_id} does not exist.")
            league["Teams"] = teams
        return jsonify({
            league
        })
    else:
        return abort(404, description="League not found")