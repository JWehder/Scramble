import os
import sys
from datetime import datetime
from pymongo import MongoClient

# Adjust the path for accessing your Flask app directory if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.config import db
holes_collection = db.holes

def find_and_replace_holepar_documents():
    # Step 1: Find all documents with the "HolePar" attribute and store them in an array
    holepar_documents = list(holes_collection.find({"HolePar": {"$exists": False}}))

    # Step 3: Process each document in the array to calculate the correct "HolePar" value
    for hole in holepar_documents:
        if "NetScore" in hole and "Strokes" in hole:
            # Calculate par based on NetScore and Strokes
            if hole["NetScore"] == 0:
                par_value = hole["Strokes"]
            else:
                par_value = hole["Strokes"] - hole["NetScore"]

            # Update the document in the database with the calculated "HolePar" value
            holes_collection.update_one(
                {"_id": hole["_id"]},
                {"$set": {"HolePar": par_value}}
            )

    print("Processing complete. All HolePar attributes corrected and re-added.")

if __name__ == "__main__":
    # clear_par_hole_errors()
    find_and_replace_holepar_documents()

    print("Par value correction complete.")
