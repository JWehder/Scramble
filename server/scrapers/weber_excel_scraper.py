import gspread
import pandas as pd
import os
import sys
from bson.objectid import ObjectId
from collections import OrderedDict
import re

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import Draft, DraftPick, Team, League, FantasyLeagueSeason
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

item_number = 1

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

# class Period(BaseModel):
# id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
# StartDate: datetime
# EndDate: datetime
# PeriodNumber: int = Field(description="whatever number field this is in the list of periods total")
# WaiverPool: Optional[List[Dict]] = []
# FantasyLeagueSeasonId: PyObjectId
# Standings: Optional[List[PyObjectId]] = []                                        
# FreeAgentSignings: Optional[List[Dict[PyObjectId, List]]] = []
# Matchups: Optional[List[Dict[PyObjectId, PyObjectId]]] = []
# Drops: Optional[Dict[PyObjectId, List]] = {}
# TournamentId: PyObjectId
# TeamResults: Optional[List[PyObjectId]] = []
# LeagueId: PyObjectId
# DraftId: Optional[PyObjectId] = None
# created_at: Optional[datetime] = None
# updated_at: Optional[datetime] = None

def apply_points_to_team():

    team_iterator_value = 0
    c_cell_counter = 34
    d_cell_counter = 34

    while c_cell_counter < 43:

        team_name = spreadsheet.acell(f'C{c_cell_counter}').value
        team_points = spreadsheet.acell(f'D{d_cell_counter}').value

        db.teams.update_one(
            {"TeamName": f"{team_name}'s team"},
            {"$set": {"Points": int(team_points)}}
        )

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
            team = Team(**pick_info['Team'])
            print(team)
            team.add_to_golfer_usage(golfer_id)
            draft_pick = DraftPick(
                TeamId=team_id,
                GolferId=golfer_id,
                RoundNumber=pick_info["RoundNumber"],
                PickNumber=pick_number,
                LeagueId=test_league["_id"],
                DraftId=current_period["DraftId"]
            )
            draft_pick.save()

            pick_number += 1
        else:
            print(golfer_id)

    print(draft_pick)

# Compile golfers' uses for each team
def compile_golfers_usage(spreadsheet):
    golfers_usage = {}

    test_tourney_id = sorted_tournaments[1]

    a_cell_counter = 3

    while a_cell_counter < 29:
        team = spreadsheet.acell(f'A{a_cell_counter}').value

        find_team = db.teams.find_one({
            "TeamName": f"{team}'s team"
        })

        golfers_usage[team] = []
        # class TeamResult(BaseModel):
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

        b_cell_counter = a_cell_counter
        a_cell_counter += 3
        while b_cell_counter < a_cell_counter:
            player = spreadsheet.acell(f'B{b_cell_counter}').value

            # Check if there's a golfer in parentheses
            if '(' in player and ')' in player:
                main_golfer, bench_golfer = re.match(r"(.+?)\s*\((.+?)\)", player).groups()
                print(main_golfer.strip())
                print(bench_golfer.strip())

                golfer_tournament_details_main = db.golfertournamentdetails.find_one({ "Name": f"{main_golfer.strip()}", "TournamentId": test_tourney_id })
                golfer_tournament_details_bench = db.golfertournamentdetails.find_one({ "Name": f"{bench_golfer.strip()}", "TournamentId": test_tourney_id })
            else:
                golfer_tournament_details = db.golfertournamentdetails.find_one({ "Name": f"{player}", "TournamentId": test_tourney_id })
                if golfer_tournament_details:
                    golfers_usage[team].append({player: golfer_tournament_details["Score"]})
                else:
                    print(f"Player not found: {player}, {test_tourney_id}")
                    golfers_usage[team].append({player: 0})
            
            b_cell_counter += 1
    
        c_cell_counter = 34
        d_cell_counter = 34

            # class Team(BaseModel):
            #     _id: Optional[PyObjectId] = Field(alias='_id')
            #     TeamName: str
            #     ProfilePicture: Optional[str] = Field(description="Profile picture for team")
            #     Golfers: Dict[PyObjectId, Dict[str, any]] = Field(default_factory=dict, description="Dictionary of golfer IDs with usage count and team status")
            #     OwnerId: PyObjectId
            #     LeagueId: PyObjectId
            #     DraftPicks: List[PyObjectId]

        # Loop through each worksheet in the spreadsheet
        # for worksheet in spreadsheet.worksheets():
        #     df = process_worksheet(worksheet)
        #     cell_number = 3
        #     while cell_number < 29:
        #         val = worksheet.acell(f'A{cell_number}').value
        #         cell_number += 3
        #         print(val)
        #     for index, row in df.iterrows():
        #         team_name = row[0].strip('"')
        #         golfers = row[1:]

        #         for golfer in golfers:
        #             if golfer:
        #                 golfer = golfer.strip()
        #                 if team_name not in golfers_usage:
        #                     golfers_usage[team_name] = {}
        #                 if golfer not in golfers_usage[team_name]:
        #                     golfers_usage[team_name][golfer] = 0
        #                 golfers_usage[team_name][golfer] += 1
        
        # Remove the newline characters from the keys
        cleaned_golfers_usage = {key.strip(): value for key, value in golfers_usage.items()}

        # processed_dict = {}

        # for manager, players in cleaned_golfers_usage.items():
        #     main_players = []
        #     bench_players = []
            
        #     for player in players:
        #         if '(' in player and ')' in player:
        #             # Split the string into the main player and the bench player
        #             main, bench = player.split('(')
        #             main = main.strip()  # Clean up whitespace
        #             bench = bench.replace(')', '').strip()  # Remove the closing parenthesis and clean up whitespace
                    
        #             # Add to respective lists
        #             main_players.append(main)
        #             bench_players.append(bench)
        #         else:
        #             main_players.append(player.strip())
            
        #     processed_dict[manager] = {
        #         'main': main_players,
        #         'bench': bench_players
        #     }

    return cleaned_golfers_usage

# Get golfers usage data
golfers_usage = compile_golfers_usage(spreadsheet)
print(golfers_usage)

# first week only:
# comb_thru_draft_values()

# take the values from the free agent draft
# parse_thru_free_agent_rounds()

# Print the usage data
# for team, golfers in golfers_usage.items():
#     print(f"Team {team}:")
#     for golfer, uses in golfers.items():
#         print(f"  {golfer}: {uses} uses")