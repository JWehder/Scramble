import os
import sys

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db
collection = db['golfertournamentdetails']

# Function to calculate the final score for "CUT" or "WD" documents if necessary
def calculate_final_score_for_cut_or_wd(document):
    # Implement your logic here if needed to determine the final score

    return document['Score']

# Iterate through all documents and update them
for doc in collection.find():
    cut_status = False
    wd_status = False
    
    if doc.get('Score') == 'CUT':
        cut_status = True
        wd_status = False
        final_score = calculate_final_score_for_cut_or_wd(doc)
        # Update the document to include the "CUT" attribute
        collection.update_one(
            {'_id': doc['_id']},
            {'$set': {'Cut': cut_status, 'Score': final_score, 'WD': wd_status}}
        )
    elif doc.get('Score') == 'WD':
        wd_status = True
        final_score = calculate_final_score_for_cut_or_wd(doc)
        # Update the document to include the "WD" attribute
        collection.update_one(
            {'_id': doc['_id']},
            {'$set': {'WD': wd_status, 'Score': final_score, 'Cut': cut_status}}
        )
    else:
        # For non-CUT and non-WD documents, set the "CUT" and "WD" attributes to false
        collection.update_one(
            {'_id': doc['_id']},
            {'$set': {'Cut': cut_status, 'WD': wd_status}}
        )

print("All documents have been updated.")