from pymongo import MongoClient
from datetime import datetime
import re
import sys
import os

# Connect to MongoDB
# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

# Define the regex pattern to match "MM/DD/YYYY (age)"
pattern = r"(\d{1,2}/\d{1,2}/\d{4}) \(\d+\)"

# Find all documents with the birthdate pattern in the specified field
for doc in db.golfers.find({"Birthdate": {"$regex": pattern}}):
    # Extract the date part using regex
    match = re.search(pattern, doc["Birthdate"])
    if match:
        date_str = match.group(1)  # Extracts the "MM/DD/YYYY" part

        # Convert the extracted date string to a datetime object
        birthdate = datetime.strptime(date_str, "%m/%d/%Y")

        # Update the document with the new datetime value
        db.golfers.update_one(
            {"_id": doc["_id"]},
            {"$set": {"Birthdate": birthdate}}
        )

        print(f"Updated document ID {doc['_id']} with birthdate {birthdate}")
