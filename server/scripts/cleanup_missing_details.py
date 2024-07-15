from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json
import re

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

not_saved_golfers = []

for json_file_path in json_files[5:]:
    # Load tournament data from JSON file
    with open(json_file_path, "r") as file:
        tournament_data = json.load(file)

    tournament = db.tournaments.find_one({"Name": tournament_data["Name"]})

    for golfer in tournament_data["Golfers"]:
        
        # split first and last name
        golfer_split_values = golfer["Name"].split(" ")
        first_name, last_name = golfer_split_values[0], ' '.join(golfer_split_values[1:])

        if "(a)" in last_name:
            # Remove "(a)" and surrounding whitespace from the string
            last_name = re.sub(r'\s*\([^)]*\)', '', last_name).strip()

        # Query the golfer collection for the first and last name
        golfer_doc = db.golfers.find_one({"FirstName": first_name, "LastName": last_name})

        if not golfer:
            print(first_name)
            print(last_name)
            print(tournament["_id"])
            continue

        golfer_details_doc = db.golfertournamentdetails.find_one({"Name": first_name + " " + last_name, "TournamentId": tournament["_id"]})

        if golfer_details_doc == None:
            print(golfer)

            # Include a TournamentDetails array
            # { TournamentDetails: [] }
            if golfer_doc and "TournamentDetails" not in golfer_doc:
                db.golfers.update_one(
                    {"_id": golfer_doc["_id"]},
                    {"$set": {"TournamentDetails": []}}
                )

            # Insert Golfer Tournament Details
            golfer_details = {
                "GolferId": golfer_doc["_id"],
                "Position": golfer.get("Position"),
                "Name": first_name + " " + last_name,
                "Score": golfer.get("Score"),
                "R1": golfer.get("R1"),
                "R2": golfer.get("R2"),
                "R3": golfer.get("R3"),
                "R4": golfer.get("R4"),
                "TotalStrokes": golfer.get("TotalStrokes"),
                "Earnings": golfer.get("Earnings"),
                "FedexPts": golfer.get("FedexPts"),
                "TournamentId": tournament["_id"],
                "Rounds": []
            }
            
            details_id = db.golfertournamentdetails.insert_one(golfer_details).inserted_id

            # Append to the TournamentDetails array
            db.golfers.update_one(
                {"_id": golfer_doc["_id"]},
                {"$push": {"TournamentDetails": details_id}}
            )

            # Add Rounds and Holes
            for round_data in golfer["Rounds"]:

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
            golfer_details_doc = db.golfertournamentdetails.find_one({ "_id": details_id })

            db.tournaments.update_one( {"_id": tournament["_id"]}, {"$push": {"Golfers": golfer_details_doc }} )

all_tournaments = list(db.tournaments.find())

for tournament in all_tournaments:
    if len(tournament["Golfers"]) < 2:
        print(tournament["Name"])


client.close()