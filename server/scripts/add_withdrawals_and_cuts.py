import os
import sys
from pymongo import UpdateOne

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.config import db

withdrawn_golfer_tournament_details_ids = set()

# Query for holes with no strokes
holes_with_no_strokes = db.holes.find({
    "Strokes": None
})

for hole in holes_with_no_strokes:
    withdrawn_golfer_tournament_details_ids.add(hole["GolferTournamentDetailsId"])

# Find golfers who were cut
golfers_who_were_cut = db.golfertournamentdetails.find({
    "$expr": {"$lt": [{"$size": "$Rounds"}, 3]}
})

golfers_who_were_cut_set = set(golfer["_id"] for golfer in golfers_who_were_cut)

# Prepare bulk operations
bulk_updates = []

# Update golfer tournament details with "WD" and "Cut" status
for golfer_details in db.golfertournamentdetails.find({}):
    golfer_details_id = golfer_details["_id"]
    name = golfer_details.get("Name", "Unknown")

    if golfer_details_id in withdrawn_golfer_tournament_details_ids:
        print(f"Withdrawn tournament details for {name}")
        bulk_updates.append(UpdateOne(
            {"_id": golfer_details_id},
            {"$set": {"Cut": False, "WD": True}}
        ))
    elif golfer_details_id in golfers_who_were_cut_set and golfer_details_id not in withdrawn_golfer_tournament_details_ids:
        print(f"{name} was cut")
        bulk_updates.append(UpdateOne(
            {"_id": golfer_details_id},
            {"$set": {"Cut": True, "WD": False}}
        ))
    else:
        bulk_updates.append(UpdateOne(
            {"_id": golfer_details_id},
            {"$set": {"Cut": False, "WD": False}}
        ))

# Execute bulk write operation
if bulk_updates:
    db.golfertournamentdetails.bulk_write(bulk_updates)