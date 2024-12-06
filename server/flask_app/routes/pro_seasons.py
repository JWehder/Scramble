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



