from flask import jsonify, abort, request, Blueprint
import sys
import os
from bson.objectid import ObjectId
from pydantic import ValidationError

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import LeagueSettings

leagues_settings_collection = db.leagueSettings
league_collection = db.leagues

league_settings_bp = Blueprint('league_settings', __name__)

@league_settings_bp.route('/leagues_settings/leagues/<league_id>', methods=['GET'])
def get_leagues_settings_by_league_id(league_id):
    """Fetches a round by ID"""
    league = league_collection.find_one({"_id": ObjectId(league_id)})
    if league:
        leagues_settings_data = league["LeagueSettings"]
        if leagues_settings_data:
            return jsonify({
                leagues_settings_data
            })
        return abort(404, description="League settings not found for this league.")
    else:
        return abort(404, description="League not found.")

@league_settings_bp.route('/leagues_settings/<leagues_settings_id>', methods=['PATCH'])
def update_leagues_settings(leagues_settings_id):
    """Update specific fields in league settings with validation before database update"""
    data = request.get_json()  # Get the partial data from the request body
    leagues_settings = leagues_settings_collection.find_one({"_id": ObjectId(leagues_settings_id)})

    if leagues_settings:
        # Merge the existing data with the new patch data
        updated_data = {**leagues_settings, **data}
        
        # Validate the merged data using the LeagueSettings model
        try:
            league_settings_instance = LeagueSettings(**updated_data)
            # If validation passes, proceed with the database update
            league_settings_instance.save()

            # Return the validated, updated instance
            return jsonify(league_settings_instance.to_dict()), 200
        except ValidationError as e:
            # If validation fails, return an error response
            return jsonify({"error": str(e)}), 400
    else:
        return abort(404, description="League settings not found.")

@league_settings_bp.route('/leagues_settings/fantasy_games/<sport_str>', methods=['GET'])
def get_leagues_settings_by_game_str(sport_str):
    """
    Get default league settings for a given fantasy game.
    :param game_str: The string representing the fantasy game (e.g., 'golf').
    :return: JSON response containing the default settings for the game.
    """
    try:
        fantasy_game = db.fantasySportsGames.find_one({"sport": sport_str})
        default_settings = LeagueSettings(fantasy_game["defaultSettings"]).to_dict()

        if not default_settings:
            return jsonify({'error': f'No default settings found for game: {sport_str}'}), 404

        return jsonify(default_settings), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
