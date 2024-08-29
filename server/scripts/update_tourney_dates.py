from datetime import datetime
from bson import ObjectId
import os
import sys

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

tournaments_collection = db.tournaments  # Replace with your collection name

def convert_string_dates_to_datetime():
    # Find all tournaments with StartDate and EndDate fields as strings
    tournaments = tournaments_collection.find({
        "$or": [
            {"StartDate": {"$type": "string"}},
            {"EndDate": {"$type": "string"}}
        ]
    })

    for tournament in tournaments:
        updates = {}
        # Convert StartDate to datetime if it's a string
        if isinstance(tournament.get('StartDate'), str):
            try:
                updates['StartDate'] = datetime.fromisoformat(tournament['StartDate'])
            except ValueError:
                print(f"Skipping invalid StartDate format for tournament ID {tournament['_id']}")

        # Convert EndDate to datetime if it's a string
        if isinstance(tournament.get('EndDate'), str):
            try:
                updates['EndDate'] = datetime.fromisoformat(tournament['EndDate'])
            except ValueError:
                print(f"Skipping invalid EndDate format for tournament ID {tournament['_id']}")

        # Update the tournament document if we have any conversions
        if updates:
            tournaments_collection.update_one(
                {"_id": tournament["_id"]},
                {"$set": updates}
            )
            print(f"Updated tournament ID {tournament['_id']} with new date types.")

if __name__ == "__main__":
    convert_string_dates_to_datetime()
    print("Date conversion complete.")