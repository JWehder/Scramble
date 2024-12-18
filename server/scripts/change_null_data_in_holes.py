import os
import sys
# Adjust the path for accessing your Flask app directory if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.config import db
holes_collection = db.holes
rounds_collection = db.rounds
golfer_tournament_details_collection = db.golfertournamentdetails

# holes with null values for strokes and netscore
holes_with_null_values = holes_collection.update_many(
    {"NetScore": None, "NetScore": None},
    {"$set": {"NetScore": 0, "Strokes": 0}}
)

# Find all golfer tournament details with "WD" set to True
withdrawn_golfer_details = golfer_tournament_details_collection.find({
    "WD": True
})

# Collect all round IDs associated with withdrawn golfers
round_ids = []
for golfer_tournament_detail in withdrawn_golfer_details:
    # Assuming each golfer detail document has a field "Rounds" containing IDs or relevant round identifiers
    round_ids.extend(golfer_tournament_detail.get("Rounds", []))

# Fetch rounds with matching IDs in round_ids
withdrawn_rounds = rounds_collection.find({
    "_id": { "$in": round_ids }
})

for withdrawn_round in withdrawn_rounds:
    holes = holes_collection.find({
        "RoundId": withdrawn_round["_id"]
    })

    holes_list = []
    for hole in holes:
        holes_list.append(hole)

    rounds_collection.update_one(
        {"_id": withdrawn_round["_id"]},
        {"$set": {"Holes": holes_list}}
    )