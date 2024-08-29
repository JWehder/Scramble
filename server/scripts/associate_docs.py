# many of the tournaments that were created with the combination of the tourney scraping tool and create_tourneys.py script did not associate records between tournaments, golfers, rounds, holes, etc.

import os
import sys

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_app.config import db

# Collection references
golfers_collection = db.golfers
tournaments_collection = db.tournaments
golfertournamentdetails_collection = db.golfertournamentdetails
rounds_collection = db.rounds
holes_collection = db.holes
golfers_collection = db.golfers

def associate_golfer_tournament_details():
    # Step 1: Associate GolferTournamentDetails with Tournament and Golfer
    golfer_tournament_details = golfertournamentdetails_collection.find()

    for detail in golfer_tournament_details:
        detail_id = detail['_id']
        tournament_id = detail['TournamentId']
        golfer_id = detail['GolferId']

        print(f"Processing GolferTournamentDetails ID {detail_id}")

        # Step 2: Associate Rounds with GolferTournamentDetails
        round_ids = detail.get('Rounds', [])
        if not round_ids:
            rounds = rounds_collection.find({"GolferTournamentDetailsId": detail_id})
            for round_doc in rounds:
                round_id = round_doc['_id']
                round_ids.append(round_id)

                hole_ids = round_doc.get('Holes', [])
                if not hole_ids:
                    # Step 3: Associate Holes with Round
                    holes = holes_collection.find({"GolferTournamentDetailsId": detail_id})
                    hole_ids = [hole['_id'] for hole in holes]

                    # Update each hole with the current round's ID
                    holes_collection.update_many(
                        {"_id": {"$in": hole_ids}},
                        {"$set": {"RoundId": round_id}}
                    )

                    # Update Round with hole documents
                    holes_list = list(holes)
                    rounds_collection.update_one(
                        {"_id": round_id},
                        {"$set": {"Holes": holes_list}}
                    )

            # Update GolferTournamentDetails with associated Round IDs
            golfertournamentdetails_collection.update_one(
                {"_id": detail_id},
                {"$set": {"Rounds": round_ids}}
            )

        # Print the updated GolferTournamentDetails
        updated_golfer_detail = golfertournamentdetails_collection.find_one({ "_id": detail_id })

        print(tournament_id)

        # Update Tournament with the new GolferTournamentDetails
        tournaments_collection.update_one(
            {"_id": tournament_id},
            {"$addToSet": {"Golfers": updated_golfer_detail}}
        )

        # Update Golfer with the new GolferTournamentDetails
        golfers_collection.update_one(
            {"_id": golfer_id},
            {"$addToSet": {"TournamentDetails": detail_id}}
        )

        print(f"Updated Tournament ID {tournament_id} and Golfer ID {golfer_id} with GolferTournamentDetails ID {detail_id}.")

    print("All documents have been successfully updated.")

if __name__ == "__main__":
    associate_golfer_tournament_details()