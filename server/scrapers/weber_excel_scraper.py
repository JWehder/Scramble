import gspread
import pandas as pd
import os
import sys
from bson.objectid import ObjectId
from collections import OrderedDict
import re

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import Draft, DraftPick, Team, League, FantasyLeagueSeason, TeamResult
from flask_app.config import db

# Initialize the gspread client with API key
gc = gspread.service_account(filename='scramble-credentials.json')

# Open the Google Sheet
spreadsheet = gc.open("Weber Fantasy Golf Spreadsheet")

# Notes
# each tournament has to be done one at a time due to API limits in sheets

# Checklist:
# Assign teams for each team in the worksheet
# Create TeamResults for each team in this particular week
# Generate results from worksheet as well as their point totals
# Figure out how to divide up drafts

# TeamResults
# id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
# TeamId: PyObjectId
# LeagueId: PyObjectId
# TournamentId: PyObjectId
# PeriodId: PyObjectId
# TotalPoints: int = 0
# GolfersScores: Dict[PyObjectId, Dict[str, int]]
# Placing: Optional[int] = 0
# PointsFromPlacing: int = 0
# created_at: Optional[datetime] = None
# updated_at: Optional[datetime] = None

# class Draft(BaseModel):
#     _id: Optional[PyObjectId] = Field(alias='_id')
#     LeagueId: str
#     StartDate: datetime
#     EndDate: Optional[datetime] = None
#     Rounds: int
#     Picks: List[PyObjectId]
#     DraftOrder: List[PyObjectId]

item_number = 0

test_league = db.leagues.find_one({ 
    "_id": ObjectId("66cfb58fcb1c3460e49138c2")
})

test_league_teams = test_league["Teams"]

current_fantasy_league_season_id = test_league["CurrentFantasyLeagueSeasonId"]

current_fantasy_league_season = db.fantasyLeagueSeasons.find_one({
    "_id": current_fantasy_league_season_id
})

current_period = db.periods.find_one({
    "_id": current_fantasy_league_season["Periods"][item_number]
})

current_draft = db.drafts.find_one({
    "_id": current_period["DraftId"]
})

sorted_tournaments = current_fantasy_league_season["Tournaments"]

golfers_usage = {}

worksheets = spreadsheet.worksheets()

spreadsheet = worksheets[item_number]

test_tourney_id = sorted_tournaments[item_number]

def apply_points_to_team():

    team_iterator_value = 0
    c_cell_counter = 34
    d_cell_counter = 34

    while c_cell_counter < 43:

        team_name = spreadsheet.acell(f'C{c_cell_counter}').value
        team_points = spreadsheet.acell(f'D{d_cell_counter}').value

        team = db.teams.find_one({
            "TeamName": f"{team_name}'s team"
        })

        total_team_points = team["Points"] + int(team_points)

        db.teams.update_one(
            {"TeamName": f"{team_name}'s team"},
            {"$set": {"Points": int(total_team_points)}}
        )

        db.teamResults.update_one({
            {"PeriodId": current_period["_id"], "TeamId": team["_id"]},
            {"$set": {"PointsFromPlacing": team_points}}
        })

        print(f"{team_name}: {team_points}")

        c_cell_counter += 1
        d_cell_counter += 1
        team_iterator_value += 1

def comb_thru_draft_values():

    j_cell_counter, k_cell_counter = 13, 13

    pick_counter = 3
    round_number = 2

    while j_cell_counter < 20 and k_cell_counter < 20:
        team_name = spreadsheet.acell(f'J{j_cell_counter}').value
        player_name = spreadsheet.acell(f'K{k_cell_counter}').value

        split_name_values = player_name.split(' ')
        first_name, last_name = split_name_values[0], ' '.join(split_name_values[1:])

        find_team = db.teams.find_one({
            "TeamName": f"{team_name}'s team"
        })

        if not find_team:
            print(f"could not find team {team_name}'s team")
            continue

        find_golfer = db.golfers.find_one({
            "FirstName": first_name, "LastName": last_name
        })

        if not find_golfer:
            print(f"could not find {first_name} {last_name}")
            continue

        team = Team(**find_team)
        print(team)
        team.add_to_golfer_usage(find_golfer["_id"])

        draft_pick = DraftPick(
            TeamId=find_team["_id"],
            GolferId=find_golfer["_id"],
            RoundNumber=round_number,
            PickNumber=pick_counter,
            LeagueId=test_league["_id"],
            DraftId=current_period["DraftId"]
        )

        draft_pick.save()

        if pick_counter == len(test_league_teams):
            pick_counter = 1
            round_number += 1
        else:
            pick_counter += 1

        j_cell_counter += 1
        k_cell_counter += 1

def parse_thru_free_agent_rounds():

    j_cell_counter, k_cell_counter = 21, 21

    pick_counter = 1

    # Initialize an OrderedDict to store the draft picks
    picks = OrderedDict()

    while spreadsheet.acell(f'J{j_cell_counter}').value:
        team_name = spreadsheet.acell(f'J{j_cell_counter}').value
        player_name = spreadsheet.acell(f'K{k_cell_counter}').value

        split_name_values = player_name.split(' ')
        first_name, last_name = split_name_values[0], ' '.join(split_name_values[1:])

        find_team = db.teams.find_one({
            "TeamName": f"{team_name}'s team"
        })

        if not find_team:
            print(f"could not find team {team_name}'s team")
            pick_counter += 1
            j_cell_counter += 1
            k_cell_counter += 1
            continue

        find_golfer = db.golfers.find_one({
            "FirstName": first_name, "LastName": last_name
        })

        if not find_golfer:
            print(f"could not find {first_name} {last_name}")
            pick_counter += 1
            j_cell_counter += 1
            k_cell_counter += 1
            continue

        # Store pick in the OrderedDict
        picks[(find_team["_id"], find_golfer["_id"])] = {
            'Team': find_team,
            'RoundNumber': current_draft["Rounds"],
            'PickNumber': pick_counter,
            'IsFreeAgent': False  # Initially set as not a free-agent pick
        }

        pick_counter += 1
        j_cell_counter += 1
        k_cell_counter += 1
    
    # Determine free-agent pickups
    # the spreadsheet lists free agent pickups
    if len(picks) > 9:
        # Mark the first N values as free-agent pickups
        num_free_agents = len(picks) - 9
        for i, key in enumerate(picks):
            if i < num_free_agents:
                picks[key]['IsFreeAgent'] = True
            else:
                break

    pick_number = 1
    # Print out the draft picks
    for (team_id, golfer_id), pick_info in picks.items():
        if not pick_info['IsFreeAgent']:
            # team = Team(**pick_info['Team'])
            # team.add_to_golfer_usage(golfer_id)
            draft_pick = DraftPick(
                TeamId=team_id,
                GolferId=golfer_id,
                RoundNumber=pick_info["RoundNumber"],
                PickNumber=pick_number,
                LeagueId=test_league["_id"],
                DraftId=current_period["DraftId"]
            )
            print(draft_pick)
            # draft_pick.save()

            pick_number += 1
        else:
            print("Free agent: ", golfer_id)
            find_team.sign_free_agent(golfer_id, current_period["_id"])

def insert_team_results(team_id):
    team = db.teams.find_one({
        "_id": team_id
    })

    team_instance = Team(**team)

    current_golfers_ids = team_instance.get_all_current_golfers_ids()

    golfer_scores = []

    team_score = 0

    curr_period = db.periods.find_one({
        "_id": current_period["_id"]
    })

    for golfer_id in current_golfers_ids:

        golfer_details = db.golfertournamentdetails.find_one({
            "GolferId": ObjectId(golfer_id),
            "TournamentId": curr_period["TournamentId"]
        })

        if not golfer_details:
            ValueError("No golfer details found for this golfer name and tournament combo. Please check your input and try again.")

        golfer_scores.append(golfer_details["_id"])

        print(team_instance.Golfers)

        score = 0

        if team_instance.Golfers[golfer_id]["IsBench"]:
            continue

        if golfer_details["Score"] == 'E':
            score = 0
        else:
            score = int(golfer_details["Score"])

        if golfer_details["Cut"] or golfer_details["WD"]:
            cut_penalty = test_league["LeagueSettings"]["CutPenalty"]
            score += cut_penalty

        team_score += score

    team_result = TeamResult(
        TeamId=team_id,
        TournamentId=test_tourney_id,
        PeriodId=current_period['_id'],
        TeamScore=team_score,
        GolfersScores= golfer_scores,
        Placing=0,
        PointsFromPlacing=0
    )

    team_result.save()

# Compile golfers' uses for each team
def compile_golfers_usage(spreadsheet):
    golfers_usage = {}

    test_tourney_id = sorted_tournaments[1]

    a_cell_counter = 3

    while a_cell_counter < 29:
        team = spreadsheet.acell(f'A{a_cell_counter}').value

        team = team.strip()
        find_team = db.teams.find_one({"TeamName": f"{team}'s team"})

        print(find_team)

        current_team = Team(**find_team)

        current_golfers_ids = current_team.get_all_current_golfers_ids()

        golfers_usage[team] = []

        b_cell_counter = a_cell_counter
        a_cell_counter += 3

        # return a bunch of golfer ids for current golfers

        scraped_golfer_ids = []

        while b_cell_counter < a_cell_counter:
            player = spreadsheet.acell(f'B{b_cell_counter}').value

            # Check if there's a golfer in parentheses
            if '(' in player and ')' in player:
                main_golfer, bench_golfer = re.match(r"(.+?)\s*\((.+?)\)", player).groups()

                golfer_tournament_details_main = db.golfertournamentdetails.find_one({ "Name": f"{main_golfer.strip()}", "TournamentId": test_tourney_id })

                main_golfer_id = golfer_tournament_details_main["GolferId"]

                print("Main golfer id: ", main_golfer_id)

                # current_team.add_to_golfer_usage(main_golfer_id)

                scraped_golfer_ids.append(str(main_golfer_id))

                bench_golfer_name = bench_golfer.strip()

                split_name_values = bench_golfer_name.split(' ')
                first_name, last_name = split_name_values[0], ' '.join(split_name_values[1:])

                bench_golfer = db.golfers.find_one({ "FirstName": first_name, "LastName": last_name })

                bench_golfer_id = bench_golfer["_id"]

                print("Bench golfer id: ", bench_golfer_id)

                # current_team.add_to_golfer_usage(bench_golfer_id, bench=True)

                # add to list of scraped ids for cross checking on teams current golfers
                scraped_golfer_ids.append(str(bench_golfer_id))
                
            else:
                golfer_tournament_details = db.golfertournamentdetails.find_one({ "Name": f"{player}", "TournamentId": test_tourney_id })
                if golfer_tournament_details:
                    golfer_id = golfer_tournament_details["GolferId"]
                    scraped_golfer_ids.append(str(golfer_id))
                    golfers_usage[team].append({player: golfer_tournament_details["Score"]})
                else:
                    print(f"Player not found: {player}, {test_tourney_id}")
                    golfers_usage[team].append({player: 0})
            
            b_cell_counter += 1

        to_remove_golfers = set(current_golfers_ids)
    
        # Iterate over the scraped golfers
        for golfer_id in scraped_golfer_ids:
            if golfer_id in current_golfers_ids:
                # add another use for the particular golfer
                current_team.add_to_golfer_usage()
                to_remove_golfers.discard(golfer_id)  # Remove from 'to_remove' set
            else:
                print("add to the team:", golfer_id)
                # new golfer, add to the team
                current_team.add_to_golfer_usage(golfer_id)
        
        # Process removal of golfers who are no longer in the scraped list
        for golfer_id in to_remove_golfers:
            # this golfer was dropped
            print("This golfer was dropped: ", golfer_id)
            current_team.remove_golfer(golfer_id)
        
        # Remove the newline characters from the keys
        cleaned_golfers_usage = {key.strip(): value for key, value in golfers_usage.items()}

        # processed_dict = {}

    return cleaned_golfers_usage

# Get golfers usage data
# golfers_usage = compile_golfers_usage(spreadsheet)
# print(golfers_usage)

for team_id in test_league_teams:
    insert_team_results(team_id)

# first week only:
# comb_thru_draft_values()

# take the values from the free agent draft
# parse_thru_free_agent_rounds()

# Print the usage data
# for team, golfers in golfers_usage.items():
#     print(f"Team {team}:")
#     for golfer, uses in golfers.items():
#         print(f"  {golfer}: {uses} uses")