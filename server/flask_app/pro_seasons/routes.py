import sys
import os
from bson.objectid import ObjectId
from .model import Team

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

pro_seasons_collection = db.proSeasons
