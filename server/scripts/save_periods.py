from pymongo import errors
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

# Find periods using a specific _id
periods_cursor = db.periods.find({"FantasyLeagueSeasonId": ObjectId("66cfb58fcb1c3460e49138c4")})

# Convert the cursor to a list and extract the IDs
period_ids = [p["_id"] for p in periods_cursor]

# Perform the update on the fantasyLeagueSeason collection
result = db.fantasyLeagueSeasons.update_one(
    {"_id": ObjectId("66cfb58fcb1c3460e49138c4")},  # Correctly formatted filter
    {"$set": {"Periods": period_ids}}               # Correctly formatted update
)

# Optional: Check if the update was successful
if result.matched_count > 0:
    print("Document found.")
    if result.modified_count > 0:
        print("Document updated successfully.")
    else:
        print("Document found but not modified.")
else:
    print("No matching document found.")