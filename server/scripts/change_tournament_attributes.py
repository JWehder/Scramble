from pymongo import MongoClient
from bson import ObjectId
import os
import sys

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.config import db

# Connect to MongoDB
tournaments_collection = db.tournaments  # Replace with your collection name

# Update all tournament documents
def update_tournament_documents():
    # Find all tournament documents
    tournaments = tournaments_collection.find({})

    for tournament in tournaments:
        # Remove the 'Golfers' field
        update_data = {
            "$unset": {"Golfers": ""}
        }

        # Rename 'ProSeason' to 'ProSeasonId' without changing the value
        if "ProSeason" in tournament:
            update_data["$set"] = {"ProSeasonId": tournament["ProSeason"]}
            update_data["$unset"]["ProSeason"] = ""


        # Update the document in the database
        tournaments_collection.update_one({"_id": tournament["_id"]}, update_data)
        print(f"Updated tournament with _id: {tournament['_id']}")

if __name__ == "__main__":
    update_tournament_documents()