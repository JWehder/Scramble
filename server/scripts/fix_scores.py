import os
import sys

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

def fix_golfer_total_scores():
    all_golfer_tournament_details = db.golfertournamentdetails.find()

    for golfer_details in all_golfer_tournament_details:
        tournament = db.tournaments.find_one({ "_id": golfer_details["TournamentId"] })

        golfer_dict = dict(golfer_details)

        if len(golfer_details['Rounds']) < 2:
            golfer_dict['WD'] = True
            golfer_dict['Cut'] = False
        elif len(golfer_details['Rounds']) == 2:
            golfer_dict['WD'] = False
            golfer_dict['Cut'] = True
        else:
            golfer_dict['WD'] = False
            golfer_dict['Cut'] = False

        score_total = 0

        for r in golfer_details["Rounds"]:
            curr_r = db.rounds.find({ "_id": r })

            score_total += curr_r["Score"] 

        {
}

def fix_golfer_scores_in_tournaments():
    pass

# Query to find rounds with less than 18 holes played
rounds_with_less_than_18_holes = db.rounds.find({"Holes": {"$exists": True, "$not": {"$size": 18}}})

tournament_ids = {}

# Iterate and print the results
for r in rounds_with_less_than_18_holes:
    if r["TournamentId"] in tournament_ids:
        tournament_ids[r["TournamentId"]].append(r["GolferTournamentDetailsId"])