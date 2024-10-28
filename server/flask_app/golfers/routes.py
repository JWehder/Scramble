from flask import jsonify, abort
from . import golfers_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId
from .model import Golfer

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from teams.model import Team, League

golfers_collection = db.golfers
teams_collection = db.teams

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

@golfers_bp.route('/golfers/available_golfers/leagues/<league_id>', methods=['GET'])
def get_available_golfers(league_id):
    """Fetches a golfer by ID"""

    league = db.leagues.find_one({
        "_id": league_id
    })

    if not league:
        return jsonify({"error": "Sorry, we do not recognize that league."}), 404
    
    league = League(**league)

    available_players = league.get_available_golfers()

    if available_players:
        return jsonify({
            available_players
        }), 200
    return jsonify({"error": "Available golfers not found. Please try again."}), 404