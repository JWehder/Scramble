from typing import List, Optional, Tuple, Dict
from pydantic import BaseModel, Field, EmailStr, validator, model_validator, field_validator, ConfigDict
from datetime import datetime, timedelta
from bson import ObjectId

# Add this line to ensure the correct path
import sys
import os
sys.path.append(os.path.dirname(__file__))
from config import db

import re
import bcrypt

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema

def get_all_tournament_ids():
    tournaments_collection = db.tournaments
    tournament_ids = tournaments_collection.distinct('_id')
    return [ObjectId(tid) for tid in tournament_ids]

class Hole(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        hole_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in hole_dict and hole_dict['_id'] is not None:
            # Update existing document
            result = db.holes.update_one({'_id': hole_dict['_id']}, {'$set': hole_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(hole_dict['_id']))
        else:
            # Insert new document
            result = db.holes.insert_one(hole_dict)
            self._id = result.inserted_id
        return self._id

    @field_validator('Strokes')
    def strokes_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Strokes must be at least 1')
        return v

    @field_validator('HoleNumber')
    def hole_number_must_be_valid(cls, v):
        if not (1 <= v <= 18):
            raise ValueError('Hole number must be between 1 and 18')
        return v


class Round(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        round_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in round_dict and round_dict['_id'] is not None:
            # Update existing document
            result = db.rounds.update_one({'_id': round_dict['_id']}, {'$set': round_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(round_dict['_id']))
        else:
            # Insert new document
            result = db.rounds.insert_one(round_dict)
            self._id = result.inserted_id
        return self.id

    @field_validator('GolferTournamentDetailsId')
    def golfer_details_exist(cls, v):
        if not db.golfertournamentdetails.find_one({"_id": v}):
            raise ValueError("No value found for that golfertournamentdetails id")
        return v

    @field_validator('Score')
    def score_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Score must be positive')
        return v

class GolferTournamentDetails(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        golfer_tournament_details_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in golfer_tournament_details_dict and golfer_tournament_details_dict['_id'] is not None:
            # Update existing document
            result = db.golfertournamentdetails.update_one({'_id': golfer_tournament_details_dict['_id']}, {'$set': golfer_tournament_details_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(golfer_tournament_details_dict['_id']))
        else:
            # Insert new document
            result = db.golfertournamentdetails.insert_one(golfer_tournament_details_dict)
            self._id = result.inserted_id
        return self.id

    @model_validator(mode='before')
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
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    EndDate: datetime
    StartDate: datetime
    Name: str
    Venue: List[str]
    City: str
    State: str
    Links: List[str]
    Purse: Optional[int] = None
    PreviousWinner: Optional[PyObjectId] = None
    Par: Optional[str] = None
    Yardage: Optional[str] = None
    IsCompleted: bool = False
    InProgress: bool = False
    Golfers: Optional[List[PyObjectId]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        tournament_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in tournament_dict and tournament_dict['_id'] is not None:
            # Update existing document
            result = db.tournaments.update_one({'_id': tournament_dict['_id']}, {'$set': tournament_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(tournament_dict['_id']))
        else:
            # Insert new document
            result = db.tournaments.insert_one(tournament_dict)
            self._id = result.inserted_id
        return self.id

    @field_validator('Par')
    def par_must_be_valid(cls, v):
        if int(v) > 80:
            raise ValueError(f'Par must be valid')
        return v


class Golfer(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        golfer_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in golfer_dict and golfer_dict['_id'] is not None:
            # Update existing document
            result = db.golfers.update_one({'_id': golfer_dict['_id']}, {'$set': golfer_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(golfer_dict['_id']))
        else:
            # Insert new document
            result = db.golfers.insert_one(golfer_dict)
            self._id = result.inserted_id
        return self.id

    @model_validator(mode='before')
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

    @field_validator('Rank', 'OWGR')
    def rank_and_owgr_must_be_valid(cls, v):
        if not v.isdigit() or int(v) <= 0:
            raise ValueError('Rank and OWGR must be positive integers')
        return v

    @field_validator('Age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be a positive integer')
        return v

    @field_validator('Earnings', 'FedexPts', 'Events', 'Rounds', 'Cuts', 'Top10s', 'Wins')
    def must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

    @field_validator('AvgScore')
    def avg_score_must_be_valid(cls, v):
        if v <= 0 or v > 120:
            raise ValueError('Average score must be a positive number and realistic')
        return v

    @field_validator('GolferPageLink')
    def must_be_valid_url(cls, v):
        if not v.startswith("http"):
            raise ValueError('Golfer page link must be a valid URL')
        return v

    @field_validator('Birthdate')
    def birthdate_must_be_valid(cls, v):
        if not isinstance(v, datetime):
            raise ValueError('Birthdate must be a valid datetime')
        return v

    @field_validator('TurnedPro')
    def turned_pro_must_be_valid_year(cls, v):
        if not v.isdigit() or int(v) < 1900 or int(v) > datetime.now().year:
            raise ValueError('TurnedPro must be a valid year')
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    Username: str
    Email: EmailStr
    Password: str
    Teams: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        # Hash the password before saving
        if self.Password:
            self.Password = self.hash_password(self.Password)
        
        # Convert the object to a dictionary with aliases and exclude unset fields
        user_dict = self.dict(by_alias=True, exclude_unset=True)
        
        if '_id' in user_dict and user_dict['_id'] is not None:
            # Update existing document
            result = db.users.update_one({'_id': user_dict['_id']}, {'$set': user_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(user_dict['_id']))
        else:
            # Insert new document
            result = db.users.insert_one(user_dict)
            self.id = result.inserted_id
        return self.id

    @field_validator('Username')
    def validate_username(cls, v):
        # Add logic to check for unique username in the database
        if any(user['User'] == v for user in db.users):
            raise ValueError('Username already exists.')
        return v

    @field_validator('Username')
    def validate_username_length(cls, v):
        # Add logic to check for unique username in the database
        if len(v) < 5:
            raise ValueError('Username must have at least 8 characters.')
        return v

    @field_validator('Email')
    def validate_email(cls, v):
        # Add logic to check for unique email in the database
        if any(user['Email'] == v for user in db.users):
            raise ValueError('Email already exists')
        return v

    @field_validator('Password')
    def validate_password(cls, v):
        # Ensure the password has at least one uppercase letter, one lowercase letter, one digit, and one special character
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$', v) or not len(v) >= 8:
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character, and must be at least 8 characters.')
        return cls.hash_password(v) 

    def check_password(plain_password: str, hashed_password: str) -> bool:
        """
        Validate a password by comparing it with the stored hashed password.

        :param plain_password: The plain text password entered by the user.
        :param hashed_password: The hashed password stored in the database.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class Week(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    WeekNumber: int
    SeasonId: PyObjectId
    Standings: List[PyObjectId]                                           
    FreeAgentSignings: List[PyObjectId]
    Matchups: List[Dict[PyObjectId, PyObjectId]]
    TournamentId: PyObjectId
    TournamentId: PyObjectId
    TeamResults: List[PyObjectId]
    LeagueId: PyObjectId
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        week_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in week_dict and week_dict['_id'] is not None:
            # Update existing document
            result = db.weeks.update_one({'_id': week_dict['_id']}, {'$set': week_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(week_dict['_id']))
        else:
            # Insert new document
            result = db.weeks.insert_one(week_dict)
            self._id = result.inserted_id
        return self.id

    @field_validator('TournamentId')
    def check_tournament_id_exists(cls, v):
        tournament = db.tournaments.find_one({"_id": v})
        if not tournament:
            raise ValueError("The tournament does not exist.")
        return v

    @field_validator('WeekNumber')
    def week_number_must_be_valid(cls, v):
        if not (1 <= v <= 52):
            raise ValueError('Week number must be between 1 and 52')
        return v

    def set_standings(self) -> bool:
        league_id = team_results[0].LeagueId
        league_settings = db.leaguessettings.find_one({"LeagueId": league_id})

        if league_settings.get("HeadToHead"):
            return False

        team_results = []
        
        for team_result_id in self.TeamResults:
            team_result_doc = db.teamresults.find_one({"_id": team_result_id})
            if team_result_doc:
                team_results.append(TeamResult(**team_result_doc))

        # Determine the scoring type from the league settings
        if team_results:

            if league_settings is None:
                raise ValueError("League settings not found.")

            # Sort team results based on TotalPoints
            sorted_team_results = sorted(team_results, key=lambda x: x.TotalPoints, reverse=True)

            # Assign placing based on sorted results
            for placing, team_result in enumerate(sorted_team_results, start=1):
                # create a variable to hold the number of points the team is expected to get based off their current place
                points_from_placing = 0

                points_per_placing_arr = league_settings.get("PointsPerPlacing")

                # number of places that add to an overall teams score in the standings
                num_of_scoring_places = len(points_per_placing_arr)

                if placing > num_of_scoring_places:
                    points_from_placing = 0
                else:
                    points_from_placing += points_per_placing_arr[placing - 1]

                db.teamresults.update_one(
                    {"_id": team_result._id},
                    {"$set": {
                        "Placing": placing, 
                        "PointsFromPlacing": points_from_placing
                        }}
                )

            # Update the standings
            self.Standings = [team_result._id for team_result in sorted_team_results]
        
        return True 

class Season(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    SeasonNumber: int
    StartDate: datetime
    EndDate: datetime
    Weeks: List[PyObjectId]
    LeagueId: PyObjectId
    Active: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        season_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in season_dict and season_dict['_id'] is not None:
            # Update existing document
            result = db.seasons.update_one({'_id': season_dict['_id']}, {'$set': season_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(season_dict['_id']))
        else:
            # Insert new document
            result = db.seasons.insert_one(season_dict)
            self._id = result.inserted_id
        return self.id

    @field_validator('StartDate', 'EndDate')
    def dates_must_be_valid(cls, v, field):
        if not isinstance(v, datetime):
            raise ValueError(f'{field.name} must be a datetime')
        return v

    @field_validator('EndDate')
    def end_date_must_be_after_start_date(cls, v, values):
        start_date = values.get('start_date')
        if start_date and v <= start_date:
            raise ValueError('End date must be after start date')
        return v

class League(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    Name: str
    CommissionerId: str
    Teams: List[str] = []
    LeagueSettingsId: PyObjectId
    Seasons: List[PyObjectId]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        league_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in league_dict and league_dict['_id'] is not None:
            # Update existing document
            result = db.leagues.update_one({'_id': league_dict['_id']}, {'$set': league_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(league_dict['_id']))
        else:
            # Insert new document
            result = db.leagues.insert_one(league_dict)
            self._id = result.inserted_id
        return self.id

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
        populate_by_name = True

class LeagueSettings(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    SnakeDraft: bool = Field(default=True, ge=1, description="the order of picks reverses with each round")
    StrokePlay: bool = Field(default=False, description="Score will match the under par score for the golfer in the tournament")
    ScorePlay: bool = Field(default=False, description="Score will accumulate based on the particular number of strokes under par the golfer receives and how many points the league agrees that type of score should receive.")
    PointsPerScore: Optional[dict] = Field(default_factory=lambda: {    'Birdies': 3,
    'Eagles': 5,
    'Pars': 1,
    'Albatross': 7,
    'Bogeys': -3,
    'DoubleBogeys': -5,
    'WorseThanDoubleBogeys': -7
    }, description="Points awarded per round performance")
    MinFreeAgentDraftRounds: int = Field(default=3, ge=1, description="Minimum number of draft rounds that need to be created each week")
    MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
    NumOfStarters: int = Field(default=2, ge=1, description="Number of starters per team")
    NumOfBenchGolfers: int = Field(default=1, ge=1, description="Number of bench players per team")
    MaxDraftedPlayers: int = Field(default=1, ge=0, description="Number of draft players per week")
    PointsPerPlacing: List[int] = Field(default_factory=lambda: [10, 8, 6, 5, 4, 3, 2, 1], description="Points awarded for placements")
    Tournaments: List[PyObjectId] = Field(default_factory = lambda: get_all_tournament_ids())
    MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
    DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
    SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
    HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    LeagueId: PyObjectId
    DefaultPointsForNonPlacers: Optional[int] = Field(default=0, description="Default points for players finishing outside the defined placements")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        league_settings_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in league_settings_dict and league_settings_dict['_id'] is not None:
            # Update existing document
            result = db.leaguesettings.update_one({'_id': league_settings_dict['_id']}, {'$set': league_settings_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(league_settings_dict['_id']))
        else:
            # Insert new document
            result = db.leaguesettings.insert_one(league_settings_dict)
            self._id = result.inserted_id
        return self.id

    @field_validator('MinFreeAgentDraftRounds')
    def max_num_of_draft_rounds(cls, v):
        if v >= cls['MaxGolfersPerTeam']:
            raise ValueError('The amount of draft rounds that have been created are more than the max amount of players allowed per team')

    @field_validator('SecondsPerDraftPick')
    def time_to_draft_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Time to draft must be a positive period of time.')
        return v

    @field_validator('NumOfStarters')
    def defined_players_must_be_less_than_max(cls, v, values):
        if 'NumOfStarters' in values and v >= values['NumOfStarters']:
            raise ValueError('Number of defined players must be less than the maximum number of golfers per team')
        return v

    @field_validator('MaxDraftedPlayers')
    def draft_players_must_fit_in_team(cls, v, values):
        if v > values['MaxGolfersPerTeam']:
            return ValueError("Your max draftable players must be less than the maximum golfers allowed on a team.")
        return v

    @field_validator('PointsPerPlacing')
    def points_per_placing_must_be_in_range(cls, v):
        if any(points < -10 or points > 10 for points in v):
            raise ValueError('Points per placing must be within the range of -10 to 10')
        return v

    @field_validator('PointsPerScore')
    def points_per_score_must_be_in_range(cls, v):
        if any(points < -10 or points > 10 for points in v.values()):
            raise ValueError('Points per score must be within the range of -10 to 10')
        return v

    @field_validator('DraftingPeriod')
    def drafting_period_must_be_valid(cls, v):
        if v not in ["weekly", "biweekly", "monthly"]:
            raise ValueError('Drafting period must be one of: "weekly", "biweekly", "monthly"')
        return v

    @field_validator('NumOfBenchGolfers')
    def bench_players_under_limit(cls, v, values):
        if v > values['MaxGolfersPerTeam'] or v > values[""]:
            return ValueError("Your number of bench golfers must be less than your starters and max amount of players allowed on a team.")
        return v

class Team(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    TeamName: str
    ProfilePicture: Optional[str] = Field(description="Profile picture for team")
    Golfers: Dict[PyObjectId, Dict[str, any]] = Field(default_factory=dict, description="Dictionary of golfer IDs with usage count and team status")
    OwnerId: PyObjectId
    LeagueId: PyObjectId
    DraftPicks: List[PyObjectId]
    Points: Optional[int] = Field(description="the amount of points that the team holds for the season based on their aggregate fantasy placings")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        team_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in team_dict and team_dict['_id'] is not None:
            # Update existing document
            result = db.teams.update_one({'_id': team_dict['_id']}, {'$set': team_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(team_dict['_id']))
        else:
            # Insert new document
            result = db.teams.insert_one(team_dict)
            self._id = result.inserted_id
        return self.id

    class Config:
        populate_by_name = True
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

class TeamResult(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    TeamId: PyObjectId
    LeagueId: PyObjectId
    TournamentId: PyObjectId
    WeekStart: datetime
    WeekEnd: datetime
    TotalPoints: int = 0
    GolfersScores: Dict[PyObjectId, Dict[str, int]]
    Placing: int = 0
    PointsFromPlacing: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        team_result_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in team_result_dict and team_result_dict['_id'] is not None:
            # Update existing document
            result = db.teamresults.update_one({'_id': team_result_dict['_id']}, {'$set': team_result_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(team_result_dict['_id']))
        else:
            # Insert new document
            result = db.teamresults.insert_one(team_result_dict)
            self._id = result.inserted_id
        return self.id
    
    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
    
    @field_validator('Placing')
    def defined_players_must_be_less_than_max(cls, v, values):
        num_of_teams_in_league = len(db.leagues.find_one({"_id": values["LeagueId"]}).Teams)
        if v > num_of_teams_in_league:
            raise ValueError('The placing the team currently is in is not possible based on the amount of teams in the league')
        return v

    def calculate_player_scores(self, db):
        league_settings = db.leaguessettings.find_one({"LeagueId": self.LeagueId})
        
        if league_settings is None:
            raise ValueError("League settings not found.")
        
        points_per_score = league_settings.get('PointsPerScore', {})
        
        for golfer_id in self.GolfersScores.items():
            golfer_details = db.golfertournamentdetails.find_one({"GolferId": golfer_id, "TournamentId": self.TournamentId})
            
            if golfer_details is None:
                continue
            
            if league_settings.get('StrokePlay'):
                self.GolfersScores[golfer_id]['TotalScore'] = golfer_details.get('TotalScore', 0)
            elif league_settings.get('ScorePlay'):
                for score_type in ['Birdies', 'Pars', 'Bogeys', 'DoubleBogeys', 'WorseThanDoubleBogeys']:
                    historical_num_of_score_type = self.GolfersScores[golfer_id].get(score_type, 0)
                    curr_num_of_score_type = golfer_details.get(score_type, 0)
                    if historical_num_of_score_type != curr_num_of_score_type:
                        difference_in_score_type_count = curr_num_of_score_type - historical_num_of_score_type
                        self.TotalPoints += (points_per_score.get(score_type, 0) * difference_in_score_type_count)
                        self.GolfersScores[golfer_id][score_type] = curr_num_of_score_type

class Draft(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    LeagueId: str
    StartDate: datetime
    EndDate: Optional[datetime] = None
    Rounds: int
    Picks: List[PyObjectId]
    DraftOrder: List[PyObjectId]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        draft_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in draft_dict and draft_dict['_id'] is not None:
            # Update existing document
            result = db.drafts.update_one({'_id': draft_dict['_id']}, {'$set': draft_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(draft_dict['_id']))
        else:
            # Insert new document
            result = db.drafts.insert_one(draft_dict)
            self._id = result.inserted_id
        return self.id

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


    @field_validator('Rounds')
    def rounds_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Number of rounds must be positive')
        return v

    @field_validator('StartDate', 'EndDate')
    def dates_must_be_valid(cls, v, field):
        if not isinstance(v, datetime):
            raise ValueError(f'{field.name} must be a valid datetime')
        return v

    @model_validator(mode='before')
    def end_date_must_be_after_start_date(cls, values):
        start_date = values.get('StartDate')
        end_date = values.get('EndDate')
        if end_date and start_date and end_date <= start_date:
            raise ValueError('End date must be after start date')
        return values

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

class DraftPick(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    TeamId: str
    GolferId: str
    RoundNumber: int
    PickNumber: int
    LeagueId: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[PyObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        draft_picks_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in draft_picks_dict and draft_picks_dict['_id'] is not None:
            # Update existing document
            result = db.draftpicks.update_one({'_id': draft_picks_dict['_id']}, {'$set': draft_picks_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(draft_picks_dict['_id']))
        else:
            # Insert new document
            result = db.draftpicks.insert_one(draft_picks_dict)
            self._id = result.inserted_id
        return self.id

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

    @model_validator(mode='before')
    def run_validations(cls, values):
        instance = cls(**values)
        instance.validate_draft_pick()
        instance.validate_pick_timing_and_order()
        return values

    @field_validator('RoundNumber', 'PickNumber')
    def pick_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Round number and pick number must be positive')
        return v

