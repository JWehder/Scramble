from pymongo import errors
import os
import json
import sys
from create_players_with_player_pages import create_golfers_in_tournament
from datetime import datetime
from bson.objectid import ObjectId

# Adjust the paths for MacOS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.models import Tournament, GolferTournamentDetails, Round, Hole
from flask_app.config import db, client

all_golfers = db.golfers.find()

for golfer in all_golfers:
    deleteable_ids = []
    for tournament_detail_id in golfer['TournamentDetails']:
        golfer_details = db.golfertournamentdetails.find_one({"_id": ObjectId(tournament_detail_id)})

        if golfer_details:
            tournament = db.tournaments.find_one({"_id": ObjectId(golfer_details['TournamentId'])})
            if tournament:
                continue

        # If golfer_details does not exist or the tournament does not exist, mark the id for deletion
        db.rounds.delete_many({"GolferTournamentDetailsId": ObjectId(tournament_detail_id)})
        db.holes.delete_many({"GolferTournamentDetailsId": ObjectId(tournament_detail_id)})
        deleteable_ids.append(ObjectId(tournament_detail_id))

    if deleteable_ids:
        # Update the golfer document to remove the identified IDs from the TournamentDetails array
        db.golfers.update_one(
            {"_id": golfer['_id']},
            {"$pull": {"TournamentDetails": {"$in": deleteable_ids}}}
        )

    print(f"Deleted TournamentDetails IDs for golfer {golfer['_id']}: {deleteable_ids}")
    

        


        