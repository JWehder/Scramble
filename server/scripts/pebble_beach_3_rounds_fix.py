from pymongo import errors
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import ValidationError

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.config import db
from flask_app.models import GolferTournamentDetails

# this script is to solve the issue with the pebble beach pro-am where there 
# were three rounds and 

tournament_details = db.golfertournamentdetails.find({
    "TournamentId": ObjectId('6631732e74d57119dcdd0a22')
})

for tournament_detail in tournament_details:

    try:
        golfer_tournament_detail = GolferTournamentDetails(**tournament_detail)

        earnings = golfer_tournament_detail.TotalStrokes
        fedex_pts = golfer_tournament_detail.Earnings
        total_strokes = golfer_tournament_detail.R4

        golfer_tournament_detail.Earnings = earnings
        golfer_tournament_detail.FedexPts = fedex_pts
        golfer_tournament_detail.TotalStrokes = total_strokes
        golfer_tournament_detail.R4 = "--"
        
        golfer_tournament_detail.save()
        print("tournament detail fixed!")
    except ValidationError as e:
        print(f"an error ocurred: {e} ")

print("done!")