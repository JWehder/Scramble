import os
import sys
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Adjust the path for accessing your Flask app directory if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.config import db
holes_collection = db.holes

def find_and_replace_holepar_documents():

    # Loop through each tournament in the collection
    for tournament in db.tournaments.find({}):

        holes = []  # This will hold hole data to be added to the tournament document

        # Find the winning golfer for the tournament (assumes winner has Position "1")
        winning_golfer_details = db.golfertournamentdetails.find_one({
            "Position": "1",
            "TournamentId": ObjectId(tournament["_id"])
        })

        # Proceed if a winning golfer is found
        if winning_golfer_details:
            # Get the last round of the winning golfer
            winning_golfer_last_round_id = winning_golfer_details["Rounds"][-1]
            last_round = db.rounds.find_one({
                "_id": ObjectId(winning_golfer_last_round_id)
            })

            if last_round:
                # Iterate through each hole in the last round
                for i, hole in enumerate(last_round["Holes"], start=1):
                    
                    # Attempt to retrieve the par value or calculate it if needed
                    par_value = hole.get("HolePar")  # Default to HolePar if available
                    if par_value is None and "NetScore" in hole and "Strokes" in hole:
                        if hole["NetScore"] is not None and hole["Strokes"] is not None:
                            # Calculate par based on NetScore and Strokes
                            par_value = hole["Strokes"] if hole["NetScore"] == 0 else hole["Strokes"] - hole["NetScore"]

                    # Construct the hole data structure
                    hole_data = {
                        "HoleNumber": i,
                        "Par": par_value,
                        "HoleType": f"Par {par_value}",
                    }

                    # Append the hole data to the list
                    holes.append(hole_data)

                # Add the holes information to the tournament document
                db.tournaments.update_one(
                    {"_id": tournament["_id"]},
                    {"$set": {"Holes": holes}}
                )

        print(f"Processed tournament: {tournament['Name']}")

    print("Processing complete. All HolePar attributes corrected and re-added.")

if __name__ == "__main__":
    # clear_par_hole_errors()
    find_and_replace_holepar_documents()

    print("Par value correction complete.")
