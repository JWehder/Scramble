from pymongo import MongoClient
import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import ProSeason

passcode = os.getenv("MONGO_PASSWORD")
test_user_username = os.getenv("TEST_USER_USERNAME")
test_user_password = os.getenv("TEST_USER_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.scramble

def create_pro_season():
    # Find the tournament with the earliest start date
    first_tournament = db.tournaments.find_one(
        {},
        sort=[("StartDate", 1)]  # Sort by StartDate in ascending order
    )

    # Find the tournament with the latest end date
    last_tournament = db.tournaments.find_one(
        {},
        sort=[("EndDate", -1)]  # Sort by EndDate in descending order
    )

    if first_tournament and last_tournament:
        # Get all tournament IDs
        tournament_ids = db.tournaments.distinct('_id')

        pro_season = ProSeason(
            League="PGA Tour",
            StartDate=first_tournament["StartDate"],
            EndDate=last_tournament["EndDate"],
            Competitions=tournament_ids,
            Active=True
        )

        pro_season_id = pro_season.save()

        print(pro_season_id)

        # Update each tournament with the ProSeason ID
        db.tournaments.update_many(
            {"_id": {"$in": tournament_ids}},
            {"$set": {"ProSeason": pro_season_id}}
        )

if __name__ == "__main__":
    create_pro_season()