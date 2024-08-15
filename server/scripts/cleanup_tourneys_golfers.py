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

all_tournaments_with_golfers = db.tournaments.find({
  "Golfers": { "$exists": True, "$not": { "$size": 0 } }
})

for tournament in all_tournaments_with_golfers:
    golfers = tournament.get("Golfers", [])
    
    # Clear the Golfers array in the tournament document
    db.tournaments.update_one({ "_id": tournament["_id"] }, { "$set": { "Golfers": [] }})

    # Iterate over each golfer in the Golfers array
    for golfer in golfers:
        golfer_id = golfer["_id"]
        
        # Delete the golfer tournament details document
        db.golfertournamentdetails.delete_one({ "_id": golfer_id })
        
        # Delete associated rounds and holes
        db.rounds.delete_many({ "GolferTournamentDetailsId": golfer_id })
        db.holes.delete_many({ "GolferTournamentDetailsId": golfer_id })

client.close()