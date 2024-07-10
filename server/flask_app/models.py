from typing import List, Optional, Tuple, Dict
from pydantic import BaseModel, Field, EmailStr, validator, root_validator
from datetime import datetime, timedelta
from bson import ObjectId
from config import db
import re

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

def get_all_tournament_ids():
    tournaments_collection = db.tournaments
    tournament_ids = tournaments_collection.distinct('_id')
    return [ObjectId(tid) for tid in tournament_ids]

class Hole(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    Strokes: int
    Par: bool
    NetScore: int
    HoleNumber: int
    Birdie: bool
    Bogey: bool
    Eagle: bool
    Albatross: bool
    DoubleBogey: bool
    WorseThanDoubleBogey: bool
    GolferTournamentDetailsId: PyObjectId
    RoundId: PyObjectId

    @validator('Strokes')
    def strokes_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Strokes must be at least 1')
        return v

    @validator('HoleNumber')
    def hole_number_must_be_valid(cls, v):
        if not (1 <= v <= 18):
            raise ValueError('Hole number must be between 1 and 18')
        return v


class Round(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    GolferTournamentDetailsId: PyObjectId
    Round: str
    Birdies: int
    Eagles: int
    Pars: int
    Albatross: int
    Bogeys: int
    DoubleBogeys: int
    WorseThanDoubleBogeys: int
    Score: int
    Holes: List[PyObjectId]

    @validator('GolferTournamentDetailsId')
    def golfer_details_exist(cls, v):
        if not db.golfertournamentdetails.find_one({"_id": v}):
            raise ValueError("No value found for that golfertournamentdetails id")

    @validator('Score')
    def score_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Score must be positive')
        return v

class GolferTournamentDetails(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    GolferId: PyObjectId
    Position: str
    Name: str
    Score: str
    R1: Optional[str] = None
    R2: Optional[str] = None
    R3: Optional[str] = None
    R4: Optional[str] = None
    TotalStrokes: Optional[str] = None
    Earnings: Optional[str] = None
    FedexPts: Optional[str] = None
    TournamentId: PyObjectId
    Rounds: List[PyObjectId]

    @root_validator(pre=True)
    def set_defaults(cls, values):
        field_defaults = {
            int: 0,
            float: 0.0,
            str: "",
            list: [],
            dict: {},
        }
        
        for field, value in values.items():
            if value is None:
                field_type = cls.__annotations__.get(field)
                if field_type in field_defaults:
                    values[field] = field_defaults[field_type]
        
        return values

class Tournament(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    EndDate: datetime
    StartDate: datetime
    Name: str
    Venue: List[str]
    City: str
    State: str
    Links: List[str]
    Purse: int
    PreviousWinner: str
    Par: str
    Yardage: str
    IsCompleted: bool
    InProgress: bool
    Golfers: List[PyObjectId]

    @validator('par')
    def par_must_be_valid(cls, v):
        valid_pars = ['3', '4', '5', '6']
        if v not in valid_pars:
            raise ValueError(f'Par must be one of {valid_pars}')
        return v

class Golfer(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    Rank: str
    FirstName: str
    LastName: str
    Age: Optional[int] = None
    Earnings: Optional[int] = None
    FedexPts: Optional[int] = None
    Events: Optional[int] = None
    Rounds: Optional[int] = None
    Flag: Optional[str] = None
    Cuts: Optional[int] = None
    Top10s: Optional[int] = None
    Wins: Optional[int] = None
    AvgScore: Optional[float] = None
    GolferPageLink: Optional[str] = None
    Birthdate: Optional[datetime] = None
    Birthplace: Optional[str] = None
    College: Optional[str] = None
    Swing: Optional[str] = None
    TurnedPro: Optional[str] = None
    TournamentDetails: Optional[List[GolferTournamentDetails]] = None
    OWGR: Optional[str] = None

    @root_validator(pre=True)
    def set_defaults(cls, values):
        field_defaults = {
            int: 0,
            float: 0.0,
            str: "",
            list: [],
            dict: {},
        }
        
        for field, value in values.items():
            if value is None:
                field_type = cls.__annotations__.get(field)
                if field_type in field_defaults:
                    values[field] = field_defaults[field_type]
        
        return values

    @validator('Rank', 'OWGR')
    def rank_and_owgr_must_be_valid(cls, v):
        if not v.isdigit() or int(v) <= 0:
            raise ValueError('Rank and OWGR must be positive integers')
        return v

    @validator('Age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be a positive integer')
        return v

    @validator('Earnings', 'FedexPts', 'Events', 'Rounds', 'Cuts', 'Top10s', 'Wins')
    def must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

    @validator('AvgScore')
    def avg_score_must_be_valid(cls, v):
        if v <= 0 or v > 120:
            raise ValueError('Average score must be a positive number and realistic')
        return v

    @validator('GolferPageLink')
    def must_be_valid_url(cls, v):
        if not v.startswith("http"):
            raise ValueError('Golfer page link must be a valid URL')
        return v

    @validator('Birthdate')
    def birthdate_must_be_valid(cls, v):
        if not isinstance(v, datetime):
            raise ValueError('Birthdate must be a valid datetime')
        return v

    @validator('TurnedPro')
    def turned_pro_must_be_valid_year(cls, v):
        if not v.isdigit() or int(v) < 1900 or int(v) > datetime.now().year:
            raise ValueError('TurnedPro must be a valid year')
        return v

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class User(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    Username: str
    Email: EmailStr
    Password: str
    Teams: List[str] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    @validator('Username')
    def validate_username(cls, v):
        # Add logic to check for unique username in the database
        if any(user['User'] == v for user in db.users):
            raise ValueError('Username already exists.')
        return v

    @validator('Username')
    def validate_username(cls, v):
        # Add logic to check for unique username in the database
        if len(v) < 8:
            raise ValueError('Username must have at least 8 characters.')
        return v

    @validator('Email')
    def validate_email(cls, v):
        # Add logic to check for unique email in the database
        if any(user['Email'] == v for user in db.users):
            raise ValueError('Email already exists')
        return v

    @validator('Password')
    def validate_password(cls, v):
        # Ensure the password has at least one uppercase letter, one lowercase letter, one digit, and one special character
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$', v) or not len(v) >= 8:
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character, and must be at least 8 characters.')
        return v

class Week(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    WeekNumber: int
    SeasonId: PyObjectId
    Standings: List[PyObjectId]                                           
    FreeAgentSignings: List[PyObjectId]
    Matchups: List[Tuple[PyObjectId, PyObjectId]]

    @validator('WeekNumber')
    def week_number_must_be_valid(cls, v):
        if not (1 <= v <= 52):
            raise ValueError('Week number must be between 1 and 52')
        return v

class Season(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    SeasonNumber: int
    StartDate: datetime
    EndDate: datetime
    Weeks: List[PyObjectId]
    LeagueId: PyObjectId
    Active: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")

    @validator('StartDate', 'EndDate')
    def dates_must_be_valid(cls, v, field):
        if not isinstance(v, datetime):
            raise ValueError(f'{field.name} must be a datetime')
        return v

    @validator('EndDate')
    def end_date_must_be_after_start_date(cls, v, values):
        start_date = values.get('start_date')
        if start_date and v <= start_date:
            raise ValueError('End date must be after start date')
        return v

class League(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    Name: str
    CommissionerId: str
    Teams: List[str] = []
    LeagueSettingsId: PyObjectId
    Seasons: List[PyObjectId]

    def get_available_players(self) -> List[PyObjectId]:
        unavailable_players = set()
        for team in self.Teams:
            for golfer_id, golfer_info in team.Golfers.items():
                if golfer_info['CurrentlyOnTeam']:
                    unavailable_players.add(golfer_id)
        # Retrieve all golfers
        all_golfers = list(db.golfers.find({}))

        # If you only need the IDs
        all_golfer_ids = [golfer['_id'] for golfer in all_golfers]
        available_players = [golfer_id for golfer_id in all_golfer_ids if golfer_id not in unavailable_players]
        return available_players

    class Config:
        allow_population_by_field_name = True

class LeagueSettings(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    SnakeDraft: bool = Field(default=True, ge=1, description="the order of picks reverses with each round")
    MinFreeAgentDraftRounds: int = Field(default=3, ge=1, description="Minimum number of draft rounds that need to be created each week")
    MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
    NumOfStarters: int = Field(default=2, ge=1, description="Number of starters per team")
    NumOfBenchGolfers: int = Field(default=1, ge=1, description="Number of bench players per team")
    MaxDraftedPlayers: int = Field(default=1, ge=0, description="Number of draft players per week")
    ScoringSystem: List[int] = Field(default_factory=lambda: [10, 8, 6, 5, 4, 3, 2, 1], description="Points awarded for placements")
    Tournaments: List[PyObjectId] = Field(default_factory = lambda: get_all_tournament_ids())
    MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
    DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
    SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
    HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    LeagueId: PyObjectId

    @validator('MinFreeAgentDraftRounds')
    def max_num_of_draft_rounds(cls, v):
        if v >= cls['MaxGolfersPerTeam']:
            raise ValueError('The amount of draft rounds that have been created are more than the max amount of players allowed per team')

    @validator('SecondsPerDraftPick')
    def time_to_draft_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Time to draft must be a positive period of time.')
        return v

    @validator('NumOfStarters')
    def defined_players_must_be_less_than_max(cls, v, values):
        if 'NumOfStarters' in values and v >= values['NumOfStarters']:
            raise ValueError('Number of defined players must be less than the maximum number of golfers per team')
        return v

    @validator('MaxDraftedPlayers')
    def draft_players_must_fit_in_team(cls, v, values):
        if v > values['MaxGolfersPerTeam']:
            return ValueError("Your max draftable players must be less than the maximum golfers allowed on a team.")
        return v

    @validator('ScoringSystem')
    def scoring_system_must_be_non_negative(cls, v):
        if any(points < 0 for points in v):
            raise ValueError('Scoring system must have non-negative points')
        return v

    @validator('DraftingPeriod')
    def drafting_period_must_be_valid(cls, v):
        if v not in ["weekly", "biweekly", "monthly"]:
            raise ValueError('Drafting period must be one of: "weekly", "biweekly", "monthly"')
        return v

class Team(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    TeamName: str
    ProfilePicture: str = Field(description="Profile picture for team")
    Golfers: Dict[PyObjectId, Dict[str, any]] = Field(default_factory=dict, description="Dictionary of golfer IDs with usage count and team status")
    OwnerId: PyObjectId
    LeagueId: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    def add_to_golfer_usage(self, golfer_id: PyObjectId):
        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['UsageCount'] += 1
        else:
            self.Golfers[golfer_id] = {'UsageCount': 1, 'CurrentlyOnTeam': True, 'IsStarter': False, 'IsBench': True}

    def remove_golfer(self, golfer_id: PyObjectId):
        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['CurrentlyOnTeam'] = False
            self.Golfers[golfer_id]['IsStarter'] = False
            self.Golfers[golfer_id]['IsBench'] = False

    def get_golfer_usage(self, golfer_id: PyObjectId) -> int:
        return self.Golfers.get(golfer_id, {}).get('UsageCount', 0)

    def is_golfer_on_team(self, golfer_id: PyObjectId) -> bool:
        return self.Golfers.get(golfer_id, {}).get('CurrentlyOnTeam', False)

    def set_golfer_as_starter(self, golfer_id: PyObjectId):
        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['IsStarter'] = True
            self.Golfers[golfer_id]['IsBench'] = False

    def set_golfer_as_bench(self, golfer_id: PyObjectId):
        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['IsStarter'] = False
            self.Golfers[golfer_id]['IsBench'] = True

    def total_golfers(self) -> int:
        return sum(1 for golfer in self.Golfers.values() if golfer['CurrentlyOnTeam'])

    def get_all_golfers(self, db) -> list:
        golfer_ids = list(self.Golfers.keys())
        golfers = list(db.golfers.find({"_id": {"$in": golfer_ids}}))
        
        for golfer in golfers:
            golfer_id = golfer['_id']
            golfer['usage_count'] = self.Golfers[golfer_id]['UsageCount']
            golfer['currently_on_team'] = self.Golfers[golfer_id]['CurrentlyOnTeam']
            golfer['is_starter'] = self.Golfers[golfer_id]['IsStarter']
            golfer['is_bench'] = self.Golfers[golfer_id]['IsBench']
        
        return golfers

class Draft(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    LeagueId: str
    StartDate: datetime
    EndDate: Optional[datetime] = None
    Rounds: int
    Picks: List[PyObjectId]
    DraftOrder: List[PyObjectId]

    def determine_draft_order(self):
        # Find the league document
        league = db.leagues.find_one({"_id": PyObjectId(self.LeagueId)})

        curr_week = None

        # Access the nested fields
        if league:
            # want the latest season
            latest_season = league.find_one({ "_id": league['SeasonId'] })
            
            if latest_season['Active']:
                # Assuming Weeks is a list and you want the last element of the last season
                curr_week = latest_season['Weeks'][-1] if latest_season['Weeks'] else None
            
        

                
        # if last_week:
        #     self.DraftOrder = last_week['Standings'].reversed()
        # else:
        #     self.DraftOrder = last_week['Standings'].reversed()


    @validator('Rounds')
    def rounds_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Number of rounds must be positive')
        return v

    @validator('StartDate', 'EndDate')
    def dates_must_be_valid(cls, v, field):
        if not isinstance(v, datetime):
            raise ValueError(f'{field.name} must be a valid datetime')
        return v

    @root_validator
    def end_date_must_be_after_start_date(cls, values):
        start_date = values.get('StartDate')
        end_date = values.get('EndDate')
        if end_date and start_date and end_date <= start_date:
            raise ValueError('End date must be after start date')
        return values

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class DraftPick(BaseModel):
    _id: Optional[PyObjectId] = Field(alias='_id')
    TeamId: str
    GolferId: str
    RoundNumber: int
    PickNumber: int
    LeagueId: int

    def get_league_settings(self) -> LeagueSettings:
        league_settings = db.league_settings.find_one({"LeagueId": self.LeagueId})
        if not league_settings:
            raise ValueError("League settings not found")
        return LeagueSettings(**league_settings)

    def validate_draft_pick(self):
        league_settings = self.get_league_settings()
        team_golfers_count = db.golfers.count_documents({"TeamId": self.TeamId})
        if team_golfers_count >= league_settings.MaxGolfersPerTeam:
            raise ValueError("Team already has the maximum number of golfers allowed")

    def validate_pick_timing_and_order(self):
        draft = db.drafts.find_one({"LeagueId": self.LeagueId})
        if not draft:
            raise ValueError("Draft not found")

        current_time = datetime.now()
        draft_start_time = draft['StartDate']
        pick_duration = draft.get('TimeToDraft', 7200)
        picks_per_round = len(draft['Picks']) / draft['Rounds']
        expected_pick_time = draft_start_time + timedelta(seconds=(self.RoundNumber - 1) * picks_per_round * pick_duration + (self.PickNumber - 1) * pick_duration)

        if current_time < draft_start_time or current_time > expected_pick_time + timedelta(seconds=pick_duration):
            raise ValueError("Pick is not within the allowed time period")

        if len(draft['Picks']) >= self.PickNumber + (self.RoundNumber - 1) * picks_per_round:
            raise ValueError("Invalid pick order")

    @root_validator(pre=False)
    def run_validations(cls, values):
        instance = cls(**values)
        instance.validate_draft_pick()
        instance.validate_pick_timing_and_order()
        return values

    @validator('RoundNumber', 'PickNumber')
    def pick_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Round number and pick number must be positive')
        return v

