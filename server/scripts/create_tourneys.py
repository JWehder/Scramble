from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json
import re
import sys

# Add the parent directory to the Python path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_directory)

# Now you can import models from flask_app
from flask.models import  Tournament # Replace YourModelClass with the actual class you want to import

load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB Connection
client = MongoClient(uri)
db = client.scramble

# Path to the directory containing JSON files
directory = "../results/"

# List to store the paths of all JSON files
json_files = []

# Iterate through all files in the directory
for filename in os.listdir(directory):
    # Check if the file has a JSON extension
    if filename.endswith(".json"):
        # Construct the full path to the JSON file
        json_file_path = os.path.join(directory, filename)
        # Append the file path to the list
        json_files.append(json_file_path)

# Iterate through all JSON files
for json_file_path in json_files[6:]:
    # Load tournament data from JSON file
    with open(json_file_path, "r") as file:
        tournament_data = json.load(file)
        
        # Process tournament data here
        split_full_name = tournament_data["PreviousWinner"].split(' ')
        first_name, last_name = split_full_name[0], ' '.join(split_full_name[1:])
        golfer_doc = db.golfers.find_one({ "FirstName": first_name, "LastName": last_name })

        # Insert Tournament
        tournament = Tournament(
            EndDate=tournament_data["EndDate"],
            StartDate=tournament_data["StartDate"],
            Name=tournament_data["Name"],
            Venue=tournament_data["Venue"],
            City=tournament_data["City"],
            State=tournament_data["State"],
            Links=tournament_data["Links"],
            Purse=tournament_data["Purse"],
            PreviousWinner=golfer_doc["_id"],
            Par=tournament_data["Par"],
            Yardage=tournament_data["Yardage"],
            IsCompleted=tournament_data["IsCompleted"],
            InProgress=tournament_data["InProgress"]
        )

        tournament_id = tournament.save()

        if tournament_data["Golfers"]: 
            # Iterate over golfers
            for golfer_data in tournament_data["Golfers"]:

                # split first and last name
                golfer_split_values = golfer_data["Name"].split(" ")
                first_name, last_name = golfer_split_values[0], ' '.join(golfer_split_values[1:])

                if "(a)" in last_name:
                    # Remove "(a)" and surrounding whitespace from the string
                    last_name = re.sub(r'\s*\([^)]*\)', '', last_name).strip()

                # Query the golfer collection for the first and last name
                golfer = db.golfers.find_one({"FirstName": first_name, "LastName": last_name})

                # Include a TournamentDetails array
                # { TournamentDetails: [] }
                if golfer and "TournamentDetails" not in golfer:
                    db.golfers.update_one(
                        {"_id": golfer["_id"]},
                        {"$set": {"TournamentDetails": []}}
                    )

                if not golfer:
                    print(first_name)
                    print(last_name)
                    print(tournament_id)
                    continue

                # Insert Golfer Tournament Details
                golfer_details = {
                    "GolferId": golfer["_id"],
                    "Position": golfer_data.get("Position"),
                    "Name": golfer["FirstName"] + " " + golfer["LastName"],
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

                # Append to the TournamentDetails array
                db.golfers.update_one(
                    {"_id": golfer["_id"]},
                    {"$push": {"TournamentDetails": details_id}}
                )

                # Add Rounds and Holes
                for round_data in golfer_data["Rounds"]:

                    round_id = db.rounds.insert_one({
                            "GolferTournamentDetailsId": details_id,
                            "Round": round_data["Round"],
                            "Birdies": round_data["Birdies"],
                            "Eagles": round_data["Eagles"],
                            "Pars": round_data["Pars"],
                            "Albatross": round_data["Albatross"],
                            "Bogeys": round_data["Bogeys"],
                            "DoubleBogeys": round_data["DoubleBogeys"],
                            "WorseThanDoubleBogeys": round_data["WorseThanDoubleBogeys"],
                            "Score": round_data["Score"],
                    }).inserted_id

                    for hole_data in round_data["Holes"]:
                        hole_data["GolferTournamentDetailsId"] = details_id
                        hole_data["RoundId"] = round_id
                        hole_id = db.holes.insert_one(hole_data).inserted_id

                    # find all the holes associated with this round
                    holes_documents = list(db.holes.find({ "RoundId": round_id }))

                    # Append Round reference to Golfer Tournament Details
                    db.rounds.update_one( {"_id": round_id}, {"$set": {"Holes": holes_documents}} )

                    # Append Round reference to Golfer Tournament Details
                    db.golfertournamentdetails.update_one({"_id": details_id}, {"$push": {"Rounds": round_id }})

            # Find golfers associated with this tournament
            golfers_documents = list(
                db.golfertournamentdetails.find({"TournamentId": tournament_id})
            )

            for golfer_doc in golfers_documents:
                db.tournaments.update_one( {"_id": tournament_id}, {"$push": {"Golfers": golfer_doc }} )

client.close()