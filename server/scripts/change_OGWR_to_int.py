import sys
import os

# Connect to MongoDB
# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

golfers_collection = db.golfers

# Find all golfers with "OGWR" as a string and update them to int
for golfer in golfers_collection.find({"OWGR": {"$type": "string"}}):
    golfer_id = golfer["_id"]
    try:
        # Convert OGWR from string to integer
        new_ogwr = int(golfer["OWGR"])
        
        # Update the golfer document
        golfers_collection.update_one(
            {"_id": golfer["_id"]},
            {"$set": {"OWGR": new_ogwr}}
        )
        
        print(f"Updated golfer {golfer_id} with OGWR: {new_ogwr}")
    
    except ValueError:
        print(f"Could not convert OGWR for golfer {golfer_id}: {golfer['OGWR']}")

print("OGWR update completed.")