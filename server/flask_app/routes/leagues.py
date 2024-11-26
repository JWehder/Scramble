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
    from models import Team

    try:
        league = leagues_collection.find_one({"_id": ObjectId(league_id)})
        
        if not league:
            return jsonify({"error": "League not found."}), 404

        league = League(**league)

        if len(league.Teams) > 1:
            # Convert team IDs to ObjectId
            team_ids = [ObjectId(team_id) for team_id in league.Teams]
            
            # Query to fetch all teams in one go
            teams = list(teams_collection.find({"_id": {"$in": team_ids}}).sort("Placement"))

            team_instances = []

            for team in teams:
                team_instance = Team(**team)
                team_instance.Golfers = team_instance.get_all_current_golfers()
                team_instance = team_instance.to_dict()
                team_instances.append(team_instance)
            
            # Check if all teams were found
            if len(teams) != len(league.Teams):
                missing_ids = set(team_ids) - {team["_id"] for team in teams}
                return jsonify({"error": f'Some team IDs do not exist: {missing_ids}'}), 404

            league.Teams = team_instances

        return jsonify(league.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500