import gspread
import pandas as pd
from pymongo import MongoClient
import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import LeagueSettings

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.scramble

# Initialize the gspread client with API key
gc = gspread.service_account(filename='scramble-credentials.json')

# Open the Google Sheet
spreadsheet = gc.open("Weber Fantasy Golf Spreadsheet")

# class Draft(BaseModel):
#     _id: Optional[PyObjectId] = Field(alias='_id')
#     LeagueId: str
#     StartDate: datetime
#     EndDate: Optional[datetime] = None
#     Rounds: int
#     Picks: List[PyObjectId]
#     DraftOrder: List[PyObjectId]


tournament_ids = [
    ObjectId('663168ca74d57119dcdc701d'),
    ObjectId('66315535ee741e831355a09a'),
    ObjectId('66314f78ee741e831355465c'),
    ObjectId('66316b9774d57119dcdc99ee'),
    ObjectId('66316a3474d57119dcdc852c'),
    ObjectId('66a6d5396556c7133a4bc9ea'),
    ObjectId('66a6d99d6556c7133a4c1d92'),
    ObjectId('66a6e7246556c7133a4d2da3'),
    ObjectId('66a6ebe46556c7133a4d8bb2'),
    ObjectId('66a6f06a6556c7133a4de15d'),
    ObjectId('66a6f9b16556c7133a4e9c39'),
    ObjectId('66a6fbca6556c7133a4ec6fc'),
    ObjectId('66a6d7576556c7133a4bf2d5'),
    ObjectId('66a172dcf47cd3eec71b0d05'),
    ObjectId('66a6e7246556c7133a4d2da3')
]

# PGA Championship

for tournament_id in tournament_ids:
    tournament = db.tournaments.find_one({ "_id": tournament_id })
    print(tournament["Name"])

# Function to process each worksheet
def process_worksheet(worksheet):
    # Get all values from the worksheet
    rows = worksheet.get_all_values()
    # Convert to a pandas DataFrame
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df

# class Season(BaseModel):
#     _id: Optional[PyObjectId] = Field(alias='_id')
#     SeasonNumber: int
#     StartDate: datetime
#     EndDate: datetime
#     Weeks: List[PyObjectId]
#     LeagueId: PyObjectId
#     Active: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")

# class League(BaseModel):
    
#     Name: str
#     CommissionerId: str
#     Teams: List[str] = []
#     LeagueSettingsId: PyObjectId
#     Seasons: List[PyObjectId]

# Username: str
# Email: EmailStr
# Password: str
# Teams: List[str] = []
# created_at: Optional[datetime] = None
# updated_at: Optional[datetime] = None

user_id = User(
    
)

league = League(
    Name="Weber",
    CommissionerId=
)


LeagueSettings = LeagueSettings(
    SnakeDraft=True,
    StrokePlay=True,
    ScorePlay=False,
    PointsPerScore=[],
    MinFreeAgentDraftRounds=1,
    ForceDrops=1,
    DropDeadline="Tuesday",
    TimeZone="US/Eastern",
    MaxGolfersPerTeam=4,
    WaiverType="Reverse Standings",
    NumberOfTeams=9
    NumOfStarters=3,
    NumOfBenchGolfers=1,
    MaxDraftedPlayers=1,
    PointsPerPlacing=[10, 8, 6, 5, 4, 3, 2, 1, 0],
    Tournaments= tournaments,
    MaxNumberOfGolferUses=None,
    DraftingFrequency=len(tournaments),
    DraftStartDayOfWeek="Wednesday",
    WaiverDeadline="Wednesday",
    SecondsPerDraftPick=3600,
    HeadToHead=False
    # DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
    # SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
    # HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    # LeagueId: PyObjectId
    # DefaultPointsForNonPlacers: Optional[int] = Field(default=0, description="Default points for players finishing outside the defined placements")
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None
)

    LeagueId: PyObjectId
    DefaultPointsForNonPlacers: Optional[int] = Field(default=0, description="Default points for players finishing outside the defined placements")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
# SnakeDraft: bool = Field(default=True, ge=1, description="the order of picks reverses with each round")
# StrokePlay: bool = Field(default=False, description="Score will match the under par score for the golfer in the tournament")
# ScorePlay: bool = Field(default=False, description="Score will accumulate based on the particular number of strokes under par the golfer receives and how many points the league agrees that type of score should receive.")
# PointsPerScore: Optional[dict] = Field(default_factory=lambda: {    'Birdies': 3,
# 'Eagles': 5,
# 'Pars': 1,
# 'Albatross': 7,
# 'Bogeys': -3,
# 'DoubleBogeys': -5,
# 'WorseThanDoubleBogeys': -7
# }, description="Points awarded per round performance")
# MinFreeAgentDraftRounds: int = Field(default=3, ge=1, description="Minimum number of draft rounds that need to be created each period")
# MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
# WaiverType: str = Field(default="Reverse Standings", description="Determine the priority with which teams receive in picking up free agents")
# NumOfStarters: int = Field(default=2, ge=1, description="Number of starters per team")
# NumOfBenchGolfers: int = Field(default=1, ge=1, description="Number of bench players per team")
# MaxDraftedPlayers: int = Field(default=1, ge=0, description="Number of draft players per period")
# PointsPerPlacing: List[int] = Field(default_factory=lambda: [10, 8, 6, 5, 4, 3, 2, 1], description="Points awarded for placements")
# Tournaments: List[PyObjectId] = Field(default_factory = lambda: get_all_tournament_ids())
# MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
# DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
# SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
# HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
# LeagueId: PyObjectId
# DefaultPointsForNonPlacers: Optional[int] = Field(default=0, description="Default points for players finishing outside the defined placements")
# created_at: Optional[datetime] = None
# updated_at: Optional[datetime] = None

# Compile golfers' uses for each team
def compile_golfers_usage(spreadsheet):
    golfers_usage = {}

    first_spreadsheet = spreadsheet.worksheets()[0]

    a_cell_counter = 3
    while a_cell_counter < 29:
        golfers_usage[first_spreadsheet.acell(f'A{a_cell_counter}').value] = {}
        # week results: 
        # class Week(BaseModel):
        #     _id: Optional[PyObjectId] = Field(alias='_id')
        #     WeekNumber: int
        #     SeasonId: PyObjectId
        #     Standings: List[PyObjectId]                                           
        #     FreeAgentSignings: List[PyObjectId]
        #     Matchups: List[Tuple[PyObjectId, PyObjectId]]
        #     TournamentId: PyObjectId

        b_cell_counter = a_cell_counter
        a_cell_counter += 3
        while b_cell_counter < a_cell_counter:
            player = first_spreadsheet.acell(f'B{b_cell_counter}').value
            print(player.split(" "))
            # golfers = db.golfers.find_one({ })

            b_cell_counter += 1
        
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
    
    # return golfers_usage

# Get golfers usage data
# golfers_usage = compile_golfers_usage(spreadsheet)

# Print the usage data
# for team, golfers in golfers_usage.items():
#     print(f"Team {team}:")
#     for golfer, uses in golfers.items():
#         print(f"  {golfer}: {uses} uses")