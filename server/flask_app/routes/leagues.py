from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import League

teams_collection = db.teams
leagues_collection = db.leagues

leagues_bp = Blueprint('leagues', __name__)

@leagues_bp.route('/<league_id>', methods=['GET'])
def get_teams_by_league_id(league_id):
    """Fetches a league by ID, including its teams."""
    try:
        league = leagues_collection.find_one({"_id": ObjectId(league_id)})
        
        if not league:
            return jsonify({"error": "League not found."}), 404

        league = League(**league)

        if len(league.Teams) > 1:
            teams = []
            for team_id in league.Teams:
                team = teams_collection.find_one({"_id": ObjectId(team_id)})
                
                if not team:
                    return abort(404, description=f"Team id: {team_id} does not exist.")
                
                teams.append(team)  # Add the team to the list

            league.Teams = teams

        return jsonify(league.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500