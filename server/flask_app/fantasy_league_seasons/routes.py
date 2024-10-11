from flask import jsonify, abort, request
from . import leagues_settings_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId
from model import FantasyLeagueSeason

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

leagues_settings_collection = db.leagueSettings
league_collection = db.leagues

@leagues_settings_bp.route('/leagues_settings/leagues/<league_id>', methods=['GET'])
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

@leagues_settings_bp.route('/leagues_settings/<leagues_settings_id>', methods=['PATCH'])
def update_leagues_settings(leagues_settings_id):
    """Update specific fields in league settings"""
    data = request.get_json()  # Get the partial data from the request body
    leagues_settings = leagues_settings_collection.find_one({"_id": ObjectId(leagues_settings_id)})
    
    if leagues_settings:
        # Update only the provided fields
        leagues_settings_collection.update_one(
            {"_id": ObjectId(leagues_settings_id)}, 
            {"$set": data}  # Only set the fields provided in 'data'
        )
        # Fetch the updated document and return it
        updated_leagues_settings = leagues_settings_collection.find_one({"_id": ObjectId(leagues_settings_id)})
        return jsonify(updated_leagues_settings), 200
    else:
        return abort(404, description="League settings not found.")