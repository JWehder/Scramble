from flask import jsonify, abort, request, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import FantasyLeagueSeason, Tournament

fantasy_league_seasons_bp = Blueprint('fantasy_league_seasons', __name__)

@fantasy_league_seasons_bp.route('/<fantasy_league_season_id>/tournaments/tournament_schedule')
def get_league_tournament_schedule(fantasy_league_season_id):
    # Find the league season and get its associated tournaments
    league_season = db.fantasyLeagueSeasons.find_one({"_id": ObjectId(fantasy_league_season_id)})

    if not league_season:
        return abort(404, description="No fantasy league season found with that ID.")

    tournament_ids = league_season.get("Tournaments", [])

    # Find all tournaments with IDs in the league season's tournaments list
    tournaments = db.tournaments.find({"_id": {"$in": [ObjectId(t_id) for t_id in tournament_ids]}})

    if tournaments:
        # Convert each tournament to a dictionary
        tournament_dicts = [Tournament(**tournament).to_dict() for tournament in tournaments]

        for tournament_dict in tournament_dicts:
            previous_winner = db.golfers.find_one({
                "_id": ObjectId(tournament_dict["PreviousWinner"])
            })
            tournament_dict["PreviousWinner"] = previous_winner["FirstName"] + previous_winner["LastName"]

        # Respond with the tournaments, or an empty array if none found
        return jsonify({"tournaments": tournament_dicts})
    else:
        return jsonify({"error": "Sorry, we could not find any tournaments for the league season you have selected."})
    