from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.scramble

# Get the absolute path to the JSON file
tournament_file = os.path.join(os.path.dirname(__file__), "..", "results", "The-Sentry.json")

# Load tournament data from JSON file
with open(tournament_file, "r") as file:
    tournament_data = json.load(file)

# Insert Tournament
tournament_id = db["tournaments"].insert_one(tournament_data).inserted_id

# Iterate over golfers
for golfer_data in tournament_data["Golfers"]:
    # split first and last name
    golfer_split_values = golfer_data["Name"].split(" ")

    first_name, last_name = golfer_split_values[0], golfer_split_values[1:]

    # Query the golfer collection for the first and last name
    golfer = db.golfers.find_one({"FirstName": first_name, "LastName": last_name})

    # Insert Golfer Tournament Details
    golfer_details = {
        "GolferId": golfer["_id"],
        "Position": golfer_data.get("Position"),
        "Name": golfer_data.get("Name"),
        "Score": golfer_data.get("Score"),
        "R1": golfer_data.get("R1"),
        "R2": golfer_data.get("R2"),
        "R3": golfer_data.get("R3"),
        "R4": golfer_data.get("R4"),
        "TotalStrokes": golfer_data.get("TotalStrokes"),
        "Earnings": golfer_data.get("Earnings"),
        "FedexPts": golfer_data.get("FedexPts"),
        "TournamentId": tournament_id,
        "Rounds": []
    }
    
    details_id = db.golfertournamentdetails.insert_one(golfer_details).inserted_id

    # Add Rounds and Holes
    for round_data in golfer_data["Rounds"]:
        round_data["GolferTournamentDetailsId"] = details_id
        round_id = db.rounds.insert_one(round_data).inserted_id

        for hole_data in round_data["Holes"]:
            hole_data["GolferTournamentDetailsId"] = details_id
            hole_data["RoundId"] = round_id
            db.holes.insert_one(hole_data)

        # Append Round reference to Golfer Tournament Details
        db.GolferTournamentDetails.update_one({"_id": details_id}, {"$push": {"Rounds": round_id}})

    # Append Golfer Tournament Details reference to Golfer
    db.golfers.update_one({"_id": golfer["_id"]}, {"$set": {"TournamentDetailsId": details_id}})

    # Add golfer back to tournament
    db.tournaments.update_one({"_id": tournament_id}, {"$push": {"golfers": golfer_data}})

client.close()
