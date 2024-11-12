from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import GolferTournamentDetails, Round


golfer_tournament_details_collection = db.golfertournamentdetails

golfer_tournament_details_bp = Blueprint('golfers_tournament_details', __name__)

@golfer_tournament_details_bp.route('/<golfers_tournament_details_id>', methods=['GET'])
def get_golfers_tournament_details(golfers_tournament_details_id):
    """Fetches a hole by ID"""
    golfer_tournament_details_data = golfer_tournament_details_collection.find_one({"_id": ObjectId(golfers_tournament_details_id)})
    if golfer_tournament_details_data:
        golfer_tournament_details = GolferTournamentDetails(**golfer_tournament_details_data)
        return jsonify({
            golfer_tournament_details
        })
    return abort(404, description="Golfer's details not found")

@golfer_tournament_details_bp.route('/golfers_tournament_details/golfer/<golfer_id>', methods=['GET'])
def get_all_tournament_details_by_golfer(golfer_id):
    """Fetch all golfer's tournament details with their id, sorted by tournament StartDate"""
    
    # Perform an aggregation to join tournament data and sort by StartDate
    all_golfers_tournament_details_data = golfer_tournament_details_collection.aggregate([
        {
            "$match": {
                "GolferId": ObjectId(golfer_id)
            }
        },
        {
            "$lookup": {
                "from": "tournaments",
                "localField": "TournamentId",
                "foreignField": "_id",
                "as": "tournament_details"
            }
        },
        {
            "$unwind": "$tournament_details"
        },
        {
            "$sort": {
                "tournament_details.StartDate": 1  # Sorting by StartDate in ascending order
            }
        },
        {
            "$project": {
                "tournament_details": 0  # Excludes tournament_details from the output
            }
        }
    ])

    golfer_details_list = list(all_golfers_tournament_details_data)
    if golfer_details_list:
        return jsonify(golfer_details_list)
    
    return abort(404, description="Sorry, no golfer details found for the specified golfer.")

@golfer_tournament_details_bp.route('/tournaments/<tournament_id>', methods=['GET'])
def get_all_golfer_tournament_details_for_tournament(tournament_id: str):
    """gets all the golfer tournament details associated with a tournament"""

    if not db.tournaments.find_one({ "_id": ObjectId(tournament_id) }):
        return jsonify({"error": "Could not find the tournament that you are looking for."}), 404

    all_golfer_tournament_details = db.golfertournamentdetails.find({
        "TournamentId": ObjectId(tournament_id)
    }).sort([("WD", 1), ("Score", 1)])

    if all_golfer_tournament_details:
        all_golfer_tournament_details_list = []

        for golfer_tournament_detail in all_golfer_tournament_details:
            golfer_tournament_detail_instance = GolferTournamentDetails(**golfer_tournament_detail)

            rounds = db.rounds.find({
                "GolferTournamentDetailsId": ObjectId(golfer_tournament_detail_instance.id)
            })
            
            # append the actual round results rather than just the id
            rounds_dicts = [(Round(**_round)).to_dict() for _round in rounds]

            # create a dict with custom method for the ability to jsonify
            golfer_tourney_details_dict = golfer_tournament_detail_instance.to_dict()

            golfer_tourney_details_dict["Rounds"] = rounds_dicts

            all_golfer_tournament_details_list.append(golfer_tourney_details_dict)

        return jsonify({
            all_golfer_tournament_details_list
        }), 200
    else:
        return jsonify({
            "error": "Sorry, we could not find golfer tournament details for this tournament."
        }), 404
