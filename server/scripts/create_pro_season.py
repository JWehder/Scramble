import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import ProSeason
from flask_app.config import db

# Fetch the documents based on tournament IDs
sorted_tournaments = list(db.tournaments.find().sort("StartDate", 1))

first_tournament = sorted_tournaments[0]
last_tournament = sorted_tournaments[-1]

sorted_tournaments_ids = [t["_id"] for t in sorted_tournaments]

pro_season = ProSeason(
    LeagueName="PGA Tour",
    StartDate=first_tournament["StartDate"],
    EndDate=last_tournament["EndDate"],
    Competitions=sorted_tournaments_ids,
    Active=True,
)

pro_season.save()