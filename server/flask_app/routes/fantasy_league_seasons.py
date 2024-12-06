from flask import jsonify, abort, request, Blueprint
import sys
import os
from bson.objectid import ObjectId
import datetime

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import FantasyLeagueSeason, Tournament

fantasy_league_seasons_bp = Blueprint('fantasy_league_seasons', __name__)

def convert_to_tournament_dicts(tournaments):

        # Convert each tournament to a dictionary
        tournament_dicts = [Tournament(**tournament).to_dict() for tournament in tournaments]

        for tournament_dict in tournament_dicts:
            if tournament_dict["IsCompleted"]:

                winner = db.golfertournamentdetails.find_one({
                    "TournamentId": ObjectId(tournament_dict["id"]),
                    "Position": "1"
                })

                tournament_dict["Winner"] = winner["Name"] + " " + f'({str(winner["Score"])})'
            else:
                previous_winner = db.golfers.find_one({
                    "_id": ObjectId(tournament_dict["PreviousWinner"])
                })

                if previous_winner:
                    tournament_dict["PreviousWinner"] = previous_winner["FirstName"] + " " + previous_winner["LastName"]
                
            if tournament_dict["Purse"] and tournament_dict["Purse"] > 0:
                tournament_dict["Purse"] = tournament_dict["Purse"] // 1000000
                tournament_dict["Purse"] = "$" + str(tournament_dict["Purse"]) + "M"
        return tournament_dicts

@fantasy_league_seasons_bp.route('/<fantasy_league_season_id>/tournaments/tournament_schedule')
def get_league_tournament_schedule(fantasy_league_season_id):
    # Find the league season and get its associated tournaments
    league_season = db.fantasyLeagueSeasons.find_one({"_id": ObjectId(fantasy_league_season_id)})

    if not league_season:
        return abort(404, description="No fantasy league season found with that ID.")

    tournament_ids = league_season.get("Tournaments", [])

    # Find all tournaments with IDs in the league season's tournaments list
    tournaments = db.tournaments.find({"_id": {"$in": [ObjectId(t_id) for t_id in tournament_ids]}}).sort("StartDate")

    if tournaments:
        # Convert each tournament to a dictionary
        tournament_dicts = [Tournament(**tournament).to_dict() for tournament in tournaments]

        for tournament_dict in tournament_dicts:
            if tournament_dict["IsCompleted"]:

                winner = db.golfertournamentdetails.find_one({
                    "TournamentId": ObjectId(tournament_dict["id"]),
                    "Position": "1"
                })

                tournament_dict["Winner"] = winner["Name"] + " " + f'({str(winner["Score"])})'
            else:
                previous_winner = db.golfers.find_one({
                    "_id": ObjectId(tournament_dict["PreviousWinner"])
                })

                if previous_winner:
                    tournament_dict["PreviousWinner"] = previous_winner["FirstName"] + " " + previous_winner["LastName"]
                
            if tournament_dict["Purse"] and tournament_dict["Purse"] > 0:
                tournament_dict["Purse"] = tournament_dict["Purse"] // 1000000
                tournament_dict["Purse"] = "$" + str(tournament_dict["Purse"]) + "M"
            

        # Respond with the tournaments, or an empty array if none found
        return jsonify({"tournaments": tournament_dicts})
    else:
        return jsonify({"error": "Sorry, we could not find any tournaments for the league season you have selected."})
    
@fantasy_league_seasons_bp.route('/<fantasy_league_season_id>/pro_season/competition_schedule')
def get_pro_season_schedule(fantasy_league_season_id):
    page = request.args.get('page', default=0, type=int)
    limit = 15  # Number of golfers per page

    # Find the fantasy league season by ID
    fantasy_league_season = db.fantasyLeagueSeasons.find_one({
        "_id": ObjectId(fantasy_league_season_id)
    })

    if not fantasy_league_season:
        return jsonify({"error": "Sorry, we do not recognize that league."}), 404

    tournament_ids = fantasy_league_season.get("Tournaments", [])

    # Find all tournaments with IDs in the league season's tournaments list
    fantasy_league_tournaments = db.tournaments.find({"_id": {"$in": [ObjectId(t_id) for t_id in tournament_ids]}}).sort("StartDate")

    current_date_time = datetime.utcnow()

    offset = page * limit

    pro_season_tournaments = db.tournaments.find(
        {"_id": {"$nin": [ObjectId(t_id) for t_id in tournament_ids]}},
        {"StartDate": {"$gt": current_date_time}}
    ).sort("StartDate").skip(offset).limit(limit=limit)

    if pro_season_tournaments and fantasy_league_tournaments:
        pro_season_tournaments_dicts = convert_to_tournament_dicts(pro_season_tournaments)
        fantasy_league_tournaments_dicts = convert_to_tournament_dicts(fantasy_league_tournaments)

        return jsonify({
            "fantasyLeagueSeasonTournaments": fantasy_league_tournaments_dicts,
            "proSeasonTournaments": pro_season_tournaments_dicts
        }), 200

    return jsonify({"error": "Sorry, we could not find the tournaments you are looking for."}), 404




    