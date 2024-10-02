from pymongo import errors
import os
import json
import sys
from datetime import datetime
from bson.objectid import ObjectId
from itertools import groupby

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.models import Period, TeamResult, Team
from flask_app.config import db, client

# manually enter in the fantasy league season
fantasy_league_season = ObjectId('66cfb58fcb1c3460e49138c4')

league_settings = db.leagueSettings.find_one({
    "_id": ObjectId('66cfb58fcb1c3460e49138c6')
})

# find all periods associated with the manually entered fantasy league season
periods = db.periods.find({
    "FantasyLeagueSeasonId": fantasy_league_season
})

# Define table headers with fixed width and align them
header = f'{"Team Name".ljust(20)} {"Period Score".ljust(15)}  {"Team Points".ljust(15)} {"Placing".ljust(10)} {"Points from Placing".ljust(20)}'

teams_points = {}

# Loop through periods and print the results
for period in periods:

    team_results_ids = period["TeamResults"]

    team_results = []

    # accumulate all of the team's results into an array
    for team_result_id in team_results_ids:
        team_result_doc = db.teamResults.find_one({"_id": team_result_id})
        if team_result_doc:
            team_results.append(TeamResult(**team_result_doc))

    period_obj = Period(**period)

    # First, sort by TeamScore (ascending)
    team_results.sort(key=lambda x: x.TeamScore)

    # Group by TeamScore (find tied teams)
    grouped_by_score = groupby(team_results, key=lambda x: x.TeamScore)

    sorted_team_results = []

    for score, tied_teams in grouped_by_score:
        tied_teams_list = list(tied_teams)

        # If there's more than one team with the same TeamScore, apply tiebreaker
        if len(tied_teams_list) > 1:
            # Sort tied teams by the highest golfer score (lower is better)
            sorted_tied_teams = sorted(
                tied_teams_list,
                key=lambda x: period_obj.get_highest_golfer_score(x)  # Tiebreaker
            )
            sorted_team_results.extend(sorted_tied_teams)
        else:
            # No tie, just append the team
            sorted_team_results.extend(tied_teams_list)

    period_number = period["PeriodNumber"]

    print(f'\nPeriod {period["PeriodNumber"]}')
    print(header)
    print('-' * len(header))  # Separator line

    for placing, team_result in enumerate(sorted_team_results, start=1):
        team = db.teams.find_one({
            "_id": team_result.TeamId
        })

        team_name = team["TeamName"]

        # Initialize the team's points and scores if not already done
        if team_name not in teams_points:
            teams_points[team_name] = 0

        # Accumulate the team's points 
        teams_points[team_name] += league_settings["PointsPerPlacing"][placing - 1]

        team_result.Placing = placing
        team_result.PointsFromPlacing = league_settings["PointsPerPlacing"][placing - 1]
        
        # team_result.save()

        # curr_team = Team(**team)

        # curr_team.Points = teams_points[team_name]
        # curr_team.save()

        # Print the team's results in table format
        print(f'{team_name.ljust(20)} {str(team_result.TeamScore).ljust(15)}  {str(teams_points[team_name]).ljust(15)} {str(team_result.Placing).ljust(10)} {str(league_settings["PointsPerPlacing"][placing - 1]).ljust(20)}')



