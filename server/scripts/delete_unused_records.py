import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

all_golfers = db.golfers.find({})

for golfer in all_golfers:
    if "TournamentDetails" not in golfer:
        continue
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

all_rounds = db.rounds.find()

for round in all_rounds:
    golfer_details = db.golfertournamentdetails.find_one({ "_id": round['GolferTournamentDetailsId'] })

    if not golfer_details:
        db.rounds.delete_many({"GolferTournamentDetailsId": ObjectId(tournament_detail_id)})
        db.holes.delete_many({"GolferTournamentDetailsId": ObjectId(tournament_detail_id)})
    

        


        
