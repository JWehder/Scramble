from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json
import re
import sys
from create_players_with_player_pages import create_golfers_in_tournament
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime

# Adjust the paths for MacOS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.models import Tournament, GolferTournamentDetails, Round # Replace YourModelClass with the actual class you want to import

# Load environment variables from .env file
load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Initialize the MongoDB client

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=30000)
    db = client.scramble
    print("Database connection successful.")
except ServerSelectionTimeoutError as e:
    print(f"Database connection failed: {e}")
# Path to the directory containing JSON files
directory = "../results/"

directory = os.path.abspath("../results/")

print(db)

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
for json_file_path in json_files:
    # Load tournament data from JSON file
    with open(json_file_path, "r") as file:
        tournament_data = json.load(file)  

        golfer_doc = None 
        
        # Process PreviousWinner
        if tournament_data.get("PreviousWinner"):
            split_full_name = tournament_data["PreviousWinner"].split(' ')
            first_name = split_full_name[0]
            last_name = ' '.join(split_full_name[1:])
            try:
                golfer_doc = db.golfers.find_one({ "FirstName": first_name, "LastName": last_name })
                print(golfer_doc["_id"])
            except Exception as e:
                print(f"Error retrieving golfer document: {e}")

        # Insert Tournament
        tournament = Tournament(
            EndDate=datetime.strptime(tournament_data["EndDate"], '%Y-%m-%dT%H:%M:%S'),
            StartDate=datetime.strptime(tournament_data["StartDate"], '%Y-%m-%dT%H:%M:%S'),
            Name=tournament_data["Name"],
            Venue=tournament_data["Venue"],
            City=tournament_data["City"],
            State=tournament_data["State"],
            Links=tournament_data["Links"],
            Purse=tournament_data["Purse"],
            PreviousWinner=golfer_doc["_id"] if golfer_doc else None,
            Par=tournament_data["Par"],
            Yardage=tournament_data["Yardage"],
            IsCompleted=tournament_data["isCompleted"],
            InProgress=tournament_data["isInProgress"]
        )

        tournament_id = tournament.save()
        print("Tournament ID:", tournament_id)

        if "Golfers" in tournament_data: 
            # if the golfers data is available, create records for them if there aren't any already.
            create_golfers_in_tournament(tournament_data["Links"][0])

            # Iterate over golfers
            for golfer_data in tournament_data["Golfers"]:

                # split first and last name
                golfer_split_values = golfer_data["Name"].split(" ")
                first_name, last_name = golfer_split_values[0], ' '.join(golfer_split_values[1:])

                if "(a)" in last_name:
                    # Remove "(a)" and surrounding whitespace from the string
                    last_name = re.sub(r'\s*\([^)]*\)', '', last_name).strip()

                # query the database for names case insensitively 
                golfer = db.golfers.find_one({
                    "FirstName": {"$regex": f"^{first_name}$", "$options": "i"},
                    "LastName": {"$regex": f"^{last_name}$", "$options": "i"}
                })

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
                golfer_details = GolferTournamentDetails(
                    GolferId= golfer["_id"],
                    Position= golfer_data.get("Position"),
                    Name= golfer["FirstName"] + " " + golfer["LastName"],
                    Score= golfer_data.get("Score"),
                    R1= golfer_data.get("R1"),
                    R2= golfer_data.get("R2"),
                    R3= golfer_data.get("R3"),
                    R4= golfer_data.get("R4"),
                    TotalStrokes= golfer_data.get("TotalStrokes"),
                    Earnings= golfer_data.get("Earnings"),
                    FedexPts= golfer_data.get("FedexPts"),
                    TournamentId= tournament_id,
                    Rounds= []
                )
                
                golfer_details_id = golfer_details.save()

                # Append to the TournamentDetails array
                db.golfers.update_one(
                    {"_id": golfer["_id"]},
                    {"$push": {"TournamentDetails": golfer_details_id}}
                )

                # Add Rounds and Holes
                for round_data in golfer_data["Rounds"]:

                    round = Round(
                            GolferTournamentDetailsId= golfer_details_id,
                            Round= round_data["Round"],
                            Birdies= round_data["Birdies"],
                            Eagles= round_data["Eagles"],
                            Pars= round_data["Pars"],
                            Albatross= round_data["Albatross"],
                            Bogeys= round_data["Bogeys"],
                            DoubleBogeys= round_data["DoubleBogeys"],
                            WorseThanDoubleBogeys= round_data["WorseThanDoubleBogeys"],
                            Score= round_data["Score"],
                    )

                    round_id = round.save()

                    for hole_data in round_data["Holes"]:
                        hole_data["GolferTournamentDetailsId"] = golfer_details_id
                        hole_data["RoundId"] = round_id
                        hole_id = db.holes.insert_one(hole_data).inserted_id

                    # find all the holes associated with this round
                    holes_documents = list(db.holes.find({ "RoundId": round_id }))

                    # Append Round reference to Golfer Tournament Details
                    db.rounds.update_one( {"_id": round_id}, {"$set": {"Holes": holes_documents}} )

                    # Append Round reference to Golfer Tournament Details
                    db.golfertournamentdetails.update_one({"_id": golfer_details_id}, {"$push": {"Rounds": round_id }})

            # Find golfers associated with this tournament
            golfers_documents = list(
                db.golfertournamentdetails.find({"TournamentId": tournament_id})
            )

            for golfer_doc in golfers_documents:
                db.tournaments.update_one( {"_id": tournament_id}, {"$push": {"Golfers": golfer_doc }} )
        else:
            db.tournaments.update_one( {"_id": tournament_id}, {"$push": {"Golfers": [] }} )