import os
import sys
from bson.objectid import ObjectId
import pymongo

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import models from flask_app
from flask_app.config import db

def process_golfer_scores(team_stats, golfers_scores):
    for golfer_detail in golfers_scores:
        if golfer_detail.get("Cut", False):
            team_stats["MissedCuts"] = team_stats.get("MissedCuts", 0) + 1

        # Handle positions with or without "T"
        position_str = golfer_detail.get("Position", "999")
        try:
            # Remove "T" if present and convert to int
            position = int(position_str.lstrip("T")) if position_str.startswith("T") else int(position_str)
        except ValueError:
            position = 999  # Default to a high value if parsing fails
        
        if position <= 10:
            team_stats["Top10s"] = team_stats.get("Top10s", 0) + 1

    return team_stats

def add_team_stats_from_period(period):
    team_results = list(db.teamResults.find({"_id": {"$in": [ObjectId(_id) for _id in period["TeamResults"]]}}))
    golfers_scores = {
        str(score["_id"]): score
        for score in db.golfertournamentdetails.find({"_id": {"$in": [ObjectId(score_id) for team in team_results for score_id in team["GolfersScores"]]}})
    }

    for team_result in team_results:
        team = db.teams.find_one({"_id": team_result["TeamId"]})
        team_stats = team.get("TeamStats", {
            "Wins": 0,
            "TotalUnderPar": 0,
            "AvgScore": 0,
            "MissedCuts": 0,
            "Top10s": 0
        })

        if team_result["Placing"] == 1:
            team_stats["Wins"] = team_stats.get("Wins", 0) + 1

        team_stats["TotalUnderPar"] = team_stats.get("TotalUnderPar", 0) + team_result["TeamScore"]
        team_stats["AvgScore"] = round(team_stats["TotalUnderPar"] / period["PeriodNumber"], 2)

        golfer_scores = [golfers_scores.get(str(g_id)) for g_id in team_result["GolfersScores"]]
        team_stats = process_golfer_scores(team_stats, golfer_scores)

        db.teams.update_one(
            {"_id": ObjectId(team["_id"])},
            {"$set": {"TeamStats": team_stats}}
        )

def add_team_stats_via_historicals(fantasy_league_season_id):
    # periods = db.periods.find({"FantasyLeagueSeasonId": ObjectId(fantasy_league_season_id)})
    # for period in periods:
    #     add_team_stats_from_period(period)

    # Fetch teams for the given FantasyLeagueSeasonId and sort them by Points
    teams = list(db.teams.find({"FantasyLeagueSeasonId": ObjectId(fantasy_league_season_id)}).sort("Points", -1))

    # Enumerate through the sorted teams and assign placements
    bulk_operations = []
    for i, team in enumerate(teams, start=1):
        bulk_operations.append(
            pymongo.UpdateOne(
                {"_id": team["_id"]},
                {"$set": {"Placement": i}}
            )
        )

    # Perform bulk update to reduce database calls
    if bulk_operations:
        db.teams.bulk_write(bulk_operations)

if __name__ == "__main__":
    add_team_stats_via_historicals(ObjectId('66cfb58fcb1c3460e49138c4'))