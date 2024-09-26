from pymongo import errors
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.models import Tournament, GolferTournamentDetails, Round, Hole
from flask_app.config import db, client

# manually enter in the fantasy league season
fantasy_league_season = ObjectId('66cfb58fcb1c3460e49138c4')

# find all periods associated with the manually entered fantasy league season
periods = db.periods.find({
    "FantasyLeagueSeasonId": fantasy_league_season
})

# Define table headers with fixed width and align them
header = f'{"Team Name".ljust(20)} {"Period Score".ljust(15)}  {"Team Points".ljust(15)} {"Placing".ljust(10)} {"Points from Placing".ljust(20)}'

teams_points = {}

# Loop through periods and print the results
for period in periods:

    period_number = period["PeriodNumber"]

    print(f"Period {period_number}")

    print(f'\nPeriod {period["PeriodNumber"]}')
    print(header)
    print('-' * len(header))  # Separator line

    for team_standings_id, team_results_id in zip(period["Standings"], period["TeamResults"]):
        team = db.teams.find_one({
            "_id": team_standings_id
        })
        team_result = db.teamResults.find_one({
            "PeriodId": period["_id"],
            "TeamId": team["_id"]
        })

        team_name = team["TeamName"]

        # Initialize the team's points and scores if not already done
        if team_name not in teams_points:
            teams_points[team_name] = 0


        # Accumulate the team's points 
        teams_points[team_name] += team_result["PointsFromPlacing"]

        # Print the team's results in table format
        print(f'{team_name.ljust(20)} {str(team_result["TeamScore"]).ljust(15)}  {str(teams_points[team_name]).ljust(15)} {str(team_result["Placing"]).ljust(10)} {str(team_result["PointsFromPlacing"]).ljust(20)}')



