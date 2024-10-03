import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.config import db
from flask_app.models import Period

def fix_existing_periods(league_id: str, season_id: str):
    # Fetch all tournaments for this season and league
    season_doc = db.fantasyLeagueSeasons.find_one({"_id": ObjectId(season_id)})
    tournament_ids = season_doc["Tournaments"]
    tournaments = list(db.tournaments.find({"_id": {"$in": tournament_ids}}).sort("StartDate"))

    if not tournaments or len(tournaments) < 2:
        raise ValueError("Insufficient tournaments to fix periods.")

    # Fetch all periods for the league
    periods = list(db.periods.find({"FantasyLeagueSeasonId": ObjectId(season_id)}).sort("PeriodNumber"))

    # Ensure the number of periods matches the number of tournaments
    if len(periods) != len(tournaments):
        print("Periods and tournaments do not match. Fixing missing periods.")
        
        # Create the missing period if necessary
        last_tournament = tournaments[-1]
        second_last_tournament = tournaments[-2]

        # Create a new period for the last tournament
        new_period = Period(
            LeagueId=league_id,
            StartDate=second_last_tournament["EndDate"],
            EndDate=last_tournament["EndDate"],
            PeriodNumber=len(periods) + 1,
            TournamentId=last_tournament["_id"],
            FantasyLeagueSeasonId=season_id
        )

        new_period_id = new_period.save()

        # Update the fantasy league season to include this new period
        db.fantasyLeagueSeasons.update_one(
            {"_id": season_id},
            {"$push": {"Periods": new_period_id}}
        )
        print(f"Created missing period for the last tournament with ID {new_period_id}.")

    # Now update all the existing periods
    for i in range(len(periods)):
        period = periods[i]
        current_tournament = tournaments[i]

        if i == 0:
            # For the first period, set StartDate to the initial league or season start date
            start_date = period["StartDate"]  # Assume the first period's start date is correct
        else:
            # Set StartDate as the EndDate of the previous tournament
            previous_tournament = tournaments[i - 1]
            start_date = previous_tournament["EndDate"]

        # Update period with correct TournamentId and dates
        db.periods.update_one(
            {"_id": period["_id"]},
            {
                "$set": {
                    "TournamentId": current_tournament["_id"],
                    "StartDate": start_date,
                    "EndDate": current_tournament["EndDate"]
                }
            }
        )

    print("Periods updated successfully.")


if __name__ == '__main__':
    fix_existing_periods('66cfb58fcb1c3460e49138c2', '66cfb58fcb1c3460e49138c4')