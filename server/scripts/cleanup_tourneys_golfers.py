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

all_tournaments = list(db.tournaments.find())

for tournament in all_tournaments:
    if len(tournament["Golfers"]) < 2:
        golfers = list(tournament["Golfers"][0])
        db.tournaments.update_one( { "_id": tournament["_id"] }, { "$set": { "Golfers": [] }} )
        for golfer in golfers:
            db.tournaments.update_one( { "_id": tournament["_id"] }, { "$push": { "Golfers": golfer }} )

client.close()