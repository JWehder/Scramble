import gspread
import pandas as pd
import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import Draft, DraftPick
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

# Compile golfers' uses for each team
def compile_golfers_usage(spreadsheet):
    golfers_usage = {}

    worksheets = spreadsheet.worksheets()

    for i in range(len(worksheets[:1])):

        spreadsheet = worksheets[i]

        test_tourney_id = sorted_tournaments[i]["_id"]

        a_cell_counter = 3
        while a_cell_counter < 29:
            team = spreadsheet.acell(f'A{a_cell_counter}').value
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

                golfer_tournament_details = db.golfertournamentdetails.find_one({ "Name": f"{player}", "TournamentId": test_tourney_id })

                if golfer_tournament_details:
                    golfers_usage[team].append({player: golfer_tournament_details["Score"]})
                else:
                    print(f"Player not found: {player}, {test_tourney_id}")
                    golfers_usage[team].append({player: 0})
                
                b_cell_counter += 1
        
        c_cell_counter = 34
        d_cell_counter = 34
        while c_cell_counter < 43:
            team_name = spreadsheet.acell(f'C{c_cell_counter}').value
            team_points = spreadsheet.acell(f'D{d_cell_counter}').value

            print(f"{team_name}: {team_points}")

            c_cell_counter += 1
            d_cell_counter += 1
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
# golfers_usage = compile_golfers_usage(spreadsheet)
# print(golfers_usage)

# Print the usage data
# for team, golfers in golfers_usage.items():
#     print(f"Team {team}:")
#     for golfer, uses in golfers.items():
#         print(f"  {golfer}: {uses} uses")