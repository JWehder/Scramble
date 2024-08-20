import os
import sys

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

# Collection references
golfers_collection = db['golfers']
golfertournamentdetails_collection = db['golfertournamentdetails']

def clear_tournament_details():
    # Step 1: Retrieve all golfers
    golfers = golfers_collection.find()

    for golfer in golfers:
        golfer_id = golfer['_id']

        # Step 2: Clear the TournamentDetails field
        golfers_collection.update_one(
            {"_id": golfer_id},
            {"$set": {"TournamentDetails": []}}
        )

        print(f"Cleared TournamentDetails for Golfer ID {golfer_id}.")

    print("All golfers have been updated with empty TournamentDetails.")

def clear_golfers_in_tournaments():
    # Step 1: Retrieve all golfers
    tournaments = db.tournaments.find()

    for tournament in tournaments:
        tournament_id = tournament['_id']

        # Step 2: Clear the TournamentDetails field
        db.tournaments.update_one(
            {"_id": tournament_id},
            {"$set": {"Golfers": []}}
        )

        print(f"Cleared TournamentDetails for Golfer ID {tournament_id}.")

    print("All golfers have been updated with empty TournamentDetails.")

if __name__ == "__main__":
    clear_tournament_details()
    clear_golfers_in_tournaments()