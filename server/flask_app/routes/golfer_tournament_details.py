from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import GolferTournamentDetails


golfer_tournament_details_collection = db.golfertournamentdetails

golfer_tournament_details_bp = Blueprint('golfers_tournament_details', __name__)

@golfer_tournament_details_bp.route('/golfers_tournament_details/<golfers_tournament_details_id>', methods=['GET'])
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