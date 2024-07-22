from flask.models import LeagueSettings
import gspread
import pandas as pd
from pymongo import MongoClient
import os

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


tournament_names = [
"THE PLAYERS Championship",
"Arnold Palmer Invitational pres. by Mastercard",
"WM Phoenix Open",
"The Genesis Invitational",
"RBC Heritage",
"Masters Tournament",
]

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
#     _id: Optional[PyObjectId] = Field(alias='_id')
#     Name: str
#     CommissionerId: str
#     Teams: List[str] = []
#     LeagueSettingsId: PyObjectId
#     Seasons: List[PyObjectId]

# class LeagueSettings(BaseModel):
#     _id: Optional[PyObjectId] = Field(alias='_id')
#     SnakeDraft: bool = Field(default=True, ge=1, description="the order of picks reverses with each round")
#     MinFreeAgentDraftRounds: int = Field(default=3, ge=1, description="Minimum number of draft rounds that need to be created each week")
#     MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
#     NumOfStarters: int = Field(default=2, ge=1, description="Number of starters per team")
#     NumOfBenchGolfers: int = Field(default=1, ge=1, description="Number of bench players per team")
#     MaxDraftedPlayers: int = Field(default=1, ge=0, description="Number of draft players per week")
#     ScoringSystem: List[int] = Field(default_factory=lambda: [10, 8, 6, 5, 4, 3, 2, 1], description="Points awarded for placements")
#     Tournaments: List[PyObjectId] = Field(default_factory = lambda: get_all_tournament_ids())
#     MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
#     DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
#     SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
#     HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
#     LeagueId: PyObjectId

league = LeagueSettings(
    # _id: Optional[PyObjectId] = Field(alias='_id')
    # SnakeDraft = True,
    # StrokePlay = True,
    # ScorePlay = False,
    # MinFreeAgentDraftRounds = 1
    # MaxGolfersPerTeam = 3,
    # NumOfStarters = 3,
    # NumOfBenchGolfers = 0,
    # MaxDraftedPlayers = 3,
    # PointsPerScore = {},
    # NumOfBenchGolfers = 2,
    # MaxDraftedPlayers = 3,
    # PointsPerPlacing = [10, 8, 7, 6, 5, 4, 3, 2, 1]
    # Tournaments: List[PyObjectId] = Field(default_factory = lambda: get_all_tournament_ids())
    # MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
    # DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
    # SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
    # HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    # LeagueId: PyObjectId
)



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
golfers_usage = compile_golfers_usage(spreadsheet)

# Print the usage data
# for team, golfers in golfers_usage.items():
#     print(f"Team {team}:")
#     for golfer, uses in golfers.items():
#         print(f"  {golfer}: {uses} uses")