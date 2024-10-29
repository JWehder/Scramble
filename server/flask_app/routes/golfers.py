from flask import jsonify, abort, request, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from ..models import Golfer, League

golfers_collection = db.golfers
teams_collection = db.teams

golfers_bp = Blueprint('golfers', __name__)

@golfers_bp.route('/golfers/<golfer_id>', methods=['GET'])
def get_golfer(golfer_id):
    """Fetches a golfer by ID"""
    golfer_data = golfers_collection.find_one({"_id": ObjectId(golfer_id)})
    if golfer_data:
        golfer = Golfer(**golfer_data)
        return jsonify({
            golfer
        })
    return abort(404, description="Golfer not found")

@golfers_bp.route('/hi', methods=['GET'])
def get_greeting():
    """Fetches a golfer by ID"""
    return jsonify({"message": "This is a super message!"})

@golfers_bp.route('/available_golfers/leagues/<league_id>', methods=['GET'])
def get_available_golfers(league_id):
    """Fetches available golfers for a league with pagination"""

    print("I'm hit!")

    # Get pagination parameters
    page = request.args.get('page', default=0, type=int)
    limit = 50  # Number of golfers per page

    # Find the league by ID
    league = db.leagues.find_one({
        "_id": ObjectId(league_id)
    })

    if not league:
        return jsonify({"error": "Sorry, we do not recognize that league."}), 404
    
    league = League(**league)

    # Get all available golfers
    available_players = league.get_available_golfers()

    # Paginate the available golfers
    if available_players:
        # Slice the list of available players for pagination
        start_index = page * limit
        end_index = start_index + limit
        paginated_players = available_players[start_index:end_index]

        # Check if there is a next page
        next_page = page + 1 if end_index < len(available_players) else None

        return jsonify({
            "golfers": paginated_players,
            "nextPage": next_page
        }), 200

    return jsonify({"error": "Available golfers not found. Please try again."}), 404
