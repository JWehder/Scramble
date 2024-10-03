import gspread
import pandas as pd
from pymongo import MongoClient
import os
import sys
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_app.models import LeagueSettings, User, League
from flask_app.config import db

test_user_username = os.getenv("TEST_USER_USERNAME")
test_user_password = os.getenv("TEST_USER_PASSWORD")

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

# Fetch the documents based on tournament IDs
sorted_tournaments = list(db.tournaments.find(
    {"_id": {"$in": tournament_ids}},
    sort=[("StartDate")] 
))

# Function to process each worksheet
def process_worksheet(worksheet):
    # Get all values from the worksheet
    rows = worksheet.get_all_values()
    # Convert to a pandas DataFrame
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


# id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
# SeasonNumber: int
# StartDate: datetime
# EndDate: datetime
# Periods: List[PyObjectId]
# LeagueId: PyObjectId
# Active: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
# created_at: Optional[datetime] = None
# updated_at: Optional[datetime] = None

def create_test_weber_league():
    user = User(
        Username=f'{test_user_username}',
        Email='jake.wehder@gmail.com',
        Password=f'{test_user_password}',
        Teams=[]
    )

    user_id = user.save()

    league = League(
        Name="Weber",
        CommissionerId=user_id,
        Teams=[],
        FantasyLeagueSeasons=[],
        CurrentFantasyLeagueSeasonId=None,
        CurrentStandings=[],
        LeagueSettings=None,
        WaiverOrder=[],
        CurrentPeriod=None
    )

    league_id = league.save()

    league.create_initial_season(sorted_tournaments)

    league.save()

    league_settings = LeagueSettings(
        SnakeDraft=True,
        StrokePlay=True,
        ScorePlay=False,
        PointsPerScore={},
        MinFreeAgentDraftRounds=1,
        ForceDrops=1,
        DropDeadline="Tuesday",
        TimeZone="US/Eastern",
        MaxGolfersPerTeam=4,
        WaiverType="Reverse Standings",
        NumberOfTeams=9,
        NumOfStarters=3,
        NumOfBenchGolfers=1,
        MaxDraftedPlayers=1,
        PointsPerPlacing=[10, 8, 7, 6, 5, 4, 3, 2, 1],
        Tournaments= tournament_ids,
        MaxNumberOfGolferUses=None,
        DraftingFrequency=1,
        DraftStartDayOfWeek="Wednesday",
        WaiverDeadline="Wednesday",
        SecondsPerDraftPick=3600,
        HeadToHead=False,
        LeagueId= league_id,
        DefaultPointsForNonPlacers= 0
    )

    print(league_settings)

    league_settings.drafting_period_must_be_valid()

    league_settings_id = league_settings.save()

    print(league_settings_id)

    league.LeagueSettings = league_settings

    league.save()

    league.create_periods_between_tournaments()
    league.create_initial_teams()


test_league = db.leagues.find_one({ "Name": "Weber" })

if not test_league: 
    create_test_weber_league()

