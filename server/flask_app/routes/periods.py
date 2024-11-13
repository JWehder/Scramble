from flask import jsonify, abort, Blueprint, request
import sys
import os
from bson.objectid import ObjectId


# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import Period

periods_collection = db.periods
team_results_collection = db.teamResults

periods_bp = Blueprint('periods', __name__)

@periods_bp.route('/fetch_participating_golfers/tournaments/<tournament_id>', methods=['POST'])
def find_period_for_league_and_tournament(tournament_id):
    data = request.get_json()
    league_id = data.get("leagueId")

    period = periods_collection.find_one({
        "LeagueId": ObjectId(league_id),
        "TournamentId": ObjectId(tournament_id)
    })

    # Assuming you have the `period` variable defined
    if period:
        golfer_tournament_details_ids = []

        # Query team_results collection for documents with the matching PeriodId
        team_results = team_results_collection.find({
            "PeriodId": period["_id"]
        })

        # Iterate over each team result document
        for team_result in team_results:
            # Retrieve the GolferScores array from each document
            golfers_scores = team_result.get("GolfersScores", [])
            
            # Collect all IDs from GolfersScores into a flat list
            for golfer_id in golfers_scores:
                golfer_tournament_details_ids.append(str(golfer_id))

        return jsonify({"golfer_scores_ids": golfer_tournament_details_ids}), 200

    else:
        jsonify({"error": "Sorry, there is currently not a period that matches the league and tournament info you entered."}), 404