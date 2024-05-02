from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB Connection
client = MongoClient(uri)
db = client.scramble

# Update all documents in the golfers collection
db.golfers.update_many(
    # Match all documents
    {},
    # Set the TournamentDetails field to an empty array
    {"$set": {"TournamentDetails": []}}
)

db.tournaments.drop()
db.golfertournamentdetails.drop()
db.holes.drop()
db.rounds.drop()

client.close()