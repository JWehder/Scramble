import sys
import os
from bson.objectid import ObjectId
from flask import Blueprint

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import ProSeason

pro_seasons_bp = Blueprint('pro_seasons', __name__)

pro_seasons_collection = db.proSeasons

@pro_seasons_bp.route('/<season_id>/competitions', methods=['GET'])
def get_pro_season_competitions(season_id):
    if not season_id:
        return {"error": "There was no season id specified."}

    pro_season = db.proSeasons.find_one({"_id": season_id})

    if not pro_season:
        return {"error": "Could not find any competitions for that particular season id."}

    pro_season_competitions_ids = [str(comp_id) for comp_id in pro_season["competitions"]]

    return 
    
