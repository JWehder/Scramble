from typing import List, Optional, Tuple, Dict
from pydantic import BaseModel, Field, EmailStr, validator, model_validator, field_validator, ConfigDict
from datetime import datetime, timedelta
from bson import ObjectId
from pymongo.client_session import ClientSession
import random

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

def get_day_number(day_name):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days.index(day_name)


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

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        hole_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in hole_dict and hole_dict['_id'] is not None:
            # Update existing document
            result = db.holes.update_one({'_id': hole_dict['_id']}, {'$set': hole_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(hole_dict['_id']))
        else:
            # Insert new document
            result = db.holes.insert_one(hole_dict, session)
            self.id = result.inserted_id
        return self.id

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
    TournamentId: PyObjectId
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        round_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in round_dict and round_dict['_id'] is not None:
            # Update existing document
            result = db.rounds.update_one(
                {'_id': round_dict['_id']}, {'$set': round_dict}, session
            )
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(round_dict['_id']))
        else:
            # Insert new document
            result = db.rounds.insert_one(round_dict, session)
            self.id = result.inserted_id
        return self.id

    @field_validator('GolferTournamentDetailsId')
    def golfer_details_exist(cls, v):
        if not db.golfertournamentdetails.find_one({"_id": v}):
            raise ValueError("No value found for that golfertournamentdetails id")
        return v

    @field_validator('Score')
    def score_must_be_positive(cls, v):
        if v < -20 or v > 70:
            raise ValueError('Score must be a realistic number.')
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

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        golfer_tournament_details_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in golfer_tournament_details_dict and golfer_tournament_details_dict['_id'] is not None:
            # Update existing document
            result = db.golfertournamentdetails.update_one({'_id': golfer_tournament_details_dict['_id']}, {'$set': golfer_tournament_details_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(golfer_tournament_details_dict['_id']))
        else:
            # Insert new document
            result = db.golfertournamentdetails.insert_one(golfer_tournament_details_dict, session)
            self.id = result.inserted_id
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

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        tournament_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in tournament_dict and tournament_dict['_id'] is not None:
            # Update existing document
            result = db.tournaments.update_one({'_id': tournament_dict['_id']}, {'$set': tournament_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(tournament_dict['_id']))
        else:
            # Insert new document
            result = db.tournaments.insert_one(tournament_dict, session)
            self.id = result.inserted_id
        return self.id

    @field_validator('Par')
    def par_must_be_valid(cls, v):
        # Check if the value is not null
        if v is not None and v != '':
            # Check if the value is a valid integer
            try:
                value = int(v)
            except ValueError:
                raise ValueError(f'Invalid value: {v}. Par must parse to a number.')

            # Ensure the numerical value is below 80
            if value > 80:
                raise ValueError(f'Invalid value: {value}. Par must be less than or equal to 80.')
        
        return v


class Golfer(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    Rank: Optional[str] = None
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
    GolferPageLink: Optional[str] = ""
    Birthdate: Optional[datetime] = None
    Birthplace: Optional[str] = ""
    HtWt: Optional[str] = ""
    College: Optional[str] = None
    Swing: Optional[str] = None
    TurnedPro: Optional[str] = None
    TournamentDetails: Optional[List[GolferTournamentDetails]] = None
    OWGR: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        golfer_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in golfer_dict and golfer_dict['_id'] is not None:
            # Update existing document
            result = db.golfers.update_one({'_id': golfer_dict['_id']}, {'$set': golfer_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(golfer_dict['_id']))
        else:
            # Insert new document
            result = db.golfers.insert_one(golfer_dict, session)
            self.id = result.inserted_id
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

    def choose_team(self, team_id: PyObjectId) -> bool:
        team = db.teams.find_one({"_id": team_id})
        if team["OwnerId"]:
            raise ValueError("Team already has an owner.")
        else:
            db.teams.update_one({"_id": team_id}, {"$set": {"OwnerId": self.id}})
            self.Teams.append(team_id)
            self.save()
            return True

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
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
            result = db.users.update_one({'_id': user_dict['_id']}, {'$set': user_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(user_dict['_id']))
        else:
            # Insert new document
            result = db.users.insert_one(user_dict, session)
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

class Period(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    StartDate: datetime
    EndDate: datetime
    PeriodNumber: int = Field(description="whatever number field this is in the list of periods total")
    WaiverPool: Optional[List[Dict]] = []
    SeasonId: PyObjectId
    Standings: Optional[List[PyObjectId]] = []                                        
    FreeAgentSignings: Optional[List[Dict[PyObjectId, List]]] = []
    Matchups: Optional[List[Dict[PyObjectId, PyObjectId]]] = []
    TournamentId: PyObjectId
    TeamResults: Optional[List[PyObjectId]] = []
    LeagueId: PyObjectId
    DraftId: Optional[PyObjectId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def add_to_waiver_pool(self, golfer_id: PyObjectId, user_id: PyObjectId, bid: int) -> bool:
        league = db.leagues.find_one({ "_id": self.LeagueId })
        league_settings = league["LeagueSettings"]
        team = db.teams.find_one({ "OwnerId": user_id, "LeagueId": self.LeagueId })

        today = datetime.utcnow()
        today = get_day_number(today.weekday())

        if today > get_day_number(league_settings.get("WaiverDeadline")):
            raise ValueError("The waiver deadline has passed.")

        if golfer_id in self.WaiverPool:
            if user_id in self.WaiverPool[golfer_id] and league_settings["WaiverType"] == "FAAB":
                self.WaiverPool[golfer_id][user_id] = bid
            elif user_id in self.WaiverPool[golfer_id] and league_settings["WaiverType"] == "Reverse Standings":
                league = League(**league)
                league.determine_waiver_order()
        else:
            self.WaiverPool[golfer_id].append({ user_id: bid if league_settings["WaiverType"] == "FAAB" else team["WaiverNumber"] })

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        period_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in period_dict and period_dict['_id'] is not None:
            # Update existing document
            result = db.periods.update_one({'_id': period_dict['_id']}, {'$set': period_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(v['_id']))
        else:
            # Insert new document
            result = db.periods.insert_one(period_dict, session)
            self.id = result.inserted_id
        return self.id

    def set_standings(self) -> bool:
        league_id = self.LeagueId
        league_settings = db.leaguessettings.find_one({"LeagueId": league_id})

        if league_settings.get("HeadToHead"):
            return False

        team_results = []
        
        for team_result_id in self.TeamResults:
            team_result_doc = db.teamresults.find_one({"_id": team_result_id})
            if team_result_doc:
                team_results.append(TeamResult(**team_result_doc))

        if team_results:
            if league_settings is None:
                raise ValueError("League settings not found.")

            sorted_team_results = sorted(team_results, key=lambda x: x.TotalPoints, reverse=True)

            for placing, team_result in enumerate(sorted_team_results, start=1):
                points_from_placing = 0

                points_per_placing_arr = league_settings.get("PointsPerPlacing")
                num_of_scoring_places = len(points_per_placing_arr)

                if placing <= num_of_scoring_places:
                    points_from_placing += points_per_placing_arr[placing - 1]

                db.teamresults.update_one(
                    {"_id": team_result._id},
                    {"$set": {
                        "Placing": placing, 
                        "PointsFromPlacing": points_from_placing
                    }}
                )

            self.Standings = [team_result._id for team_result in sorted_team_results]
            self.update({"Standings": self.Standings})
        
        return True

    @field_validator('TournamentId')
    def check_tournament_id_exists(cls, v):
        tournament = db.tournaments.find_one({"_id": v})
        if not tournament:
            raise ValueError("The tournament does not exist.")
        return v

    @field_validator('PeriodNumber')
    def period_number_must_be_valid(cls, v):
        tournament_count = db.tournaments.count_documents({})
        if not (1 <= v <= tournament_count):
            raise ValueError(f'Period number must be between 1 and the number of tournaments available to play: {tournament_count}')
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
    Periods: List[PyObjectId]
    LeagueId: PyObjectId
    Active: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        season_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in season_dict and season_dict['_id'] is not None:
            # Update existing document
            result = db.seasons.update_one({'_id': season_dict['_id']}, {'$set': season_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(season_dict['_id']))
        else:
            # Insert new document
            result = db.seasons.insert_one(season_dict, session)
            self.id = result.inserted_id
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

class LeagueSettings(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    SnakeDraft: bool = Field(default=True, ge=1, description="The order of picks reverses with each round.")
    NumberOfTeams: Optional[int] = Field(default=8, description="Number of the teams within the league.")
    StrokePlay: bool = Field(default=False, description="Score will match the under par score for the golfer in the tournament")
    ScorePlay: bool = Field(default=False, description="Score will accumulate based on the particular number of strokes under par the golfer receives and how many points the league agrees that type of score should receive.")
    ForceDrops: Optional[int] = 0
    PointsPerScore: Optional[dict] = Field(default_factory=lambda: {    'Birdies': 3,
    'Eagles': 5,
    'Pars': 1,
    'Albatross': 7,
    'Bogeys': -3,
    'DoubleBogeys': -5,
    'WorseThanDoubleBogeys': -7
    }, description="Points awarded per round performance")
    MinFreeAgentDraftRounds: int = Field(default=3, ge=1, description="Minimum number of draft rounds that need to be created each period")
    MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
    WaiverType: str = Field(default="Reverse Standings", description="Determine the priority with which teams receive in picking up free agents")
    NumOfStarters: int = Field(default=2, ge=1, description="Number of starters per team")
    NumOfBenchGolfers: int = Field(default=1, ge=1, description="Number of bench players per team")
    MaxDraftedPlayers: int = Field(default=1, ge=0, description="Number of draft players per period")
    PointsPerPlacing: Optional[List[int]] = Field(default=[], description="Points awarded for placements")
    Tournaments: List[PyObjectId] = Field(default_factory = lambda: get_all_tournament_ids())
    MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
    DraftingFrequency: int = Field(default=0, description="The number of times the league drafts in between tournaments.")
    DraftStartDayOfWeek: Optional[str] = Field(default="Monday", description="Day of the week in which the draft starts before a tournament or season.")
    WaiverDeadline: Optional[str] = Field(default = "Wednesday", description="Day of the week where players on waivers are distributed.")
    SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
    HeadToHead: bool = Field(default=False, description="Determine whether the competition is league wide or just between two users for each week.")
    LeagueId: PyObjectId
    DefaultPointsForNonPlacers: Optional[int] = Field(default=0, description="Default points for players finishing outside the defined placements")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def determine_points_per_placing(self):
        if not self.PointsPerPlacing:
            self.PointsPerPlacing = list(range(self.NumberOfTeams, 0, -1))

    # Function to determine drafting frequency options
    def determine_drafting_frequency_options(self) -> List[int]:
        # Fetch the league document using the LeagueId
        league = db.leagues.find_one({"_id": self.LeagueId})
        
        if league is None:
            raise ValueError("No league found with the provided LeagueId")
        
        num_of_tournaments = len(league['tournaments'])
        
        # Possible drafting frequency options (can be adjusted as needed)
        nums = [1, 2, 3, 4, 5]
        
        # Return the numbers that evenly divide the number of tournaments
        return [num for num in nums if num_of_tournaments % num == 0]

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        league_settings_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in league_settings_dict and league_settings_dict['_id'] is not None:
            # Update existing document
            result = db.leaguesettings.update_one({'_id': league_settings_dict['_id']}, {'$set': league_settings_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(league_settings_dict['_id']))
        else:
            # Insert new document
            result = db.leaguesettings.insert_one(league_settings_dict, session)
            self.id = result.inserted_id
        return self.id

    @field_validator('NumberOfTeams')
    def num_of_teams_is_even_num(cls, v, values):
        if v % 2 != 0 and values['HeadToHead'] == True:
            raise ValueError("The number of teams in your league must be even if you want to play a head to head league.")

    @field_validator('NumberOfTeams')
    def num_of_teams_constraint(cls, v):
        if v > 16:
            raise ValueError("There cannot be more than 16 teams in a league.")

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

    @field_validator('DraftingFrequency')
    def drafting_period_must_be_valid(cls, v, values):
        league = db.leagues.find_one({ "_id": values["LeagueId"] })
        if v > len(league["Tournaments"]):
            raise ValueError("You cannot have more drafts than you have selected tournaments")
        return v

    @field_validator('WaiverType')
    def define_waiver_fomat(cls, v):
        if v not in ["FirstToLast", "Bidding"]:
            raise ValueError("Waiver type must be either a bidding format or first to last.")
        return v

    @field_validator('NumOfBenchGolfers')
    def bench_players_under_limit(cls, v, values):
        if v > values['MaxGolfersPerTeam'] or v > values[""]:
            return ValueError("Your number of bench golfers must be less than your starters and max amount of players allowed on a team.")
        return v

    def __init__(self, **data):
        super().__init__(**data)
        self.determine_points_per_placing()

class Team(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    TeamName: str
    ProfilePicture: Optional[str] = Field(description="Profile picture for team")
    Golfers: Optional[Dict[PyObjectId, Dict[str, any]]] = Field(default_factory=dict, description="Dictionary of golfer IDs with usage count and team status")
    OwnerId: Optional[PyObjectId] = None
    LeagueId: PyObjectId
    DraftPicks: Optional[Dict[PyObjectId, PyObjectId]]
    Points: Optional[int] = Field(description="the amount of points that the team holds for the season based on their aggregate fantasy placings")
    FAAB: Optional[int] = Field(default=0, description="How much total points you have to spend on players.")
    WaiverNumber: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        team_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in team_dict and team_dict['_id'] is not None:
            # Update existing document
            result = db.teams.update_one({'_id': team_dict['_id']}, {'$set': team_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(team_dict['_id']))
        else:
            # Insert new document
            result = db.teams.insert_one(team_dict, session)
            self.id = result.inserted_id
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
            self.Golfers[golfer_id] = { 'UsageCount': 1, 'CurrentlyOnTeam': True, 'IsStarter': False, 'IsBench': True }

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

class League(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    Name: str
    CommissionerId: str
    Teams: List[PyObjectId] = []
    LeagueSettings: LeagueSettings
    Seasons: List[PyObjectId]
    CurrentStandings: Optional[List[Team]]
    WaiverOrder: Optional[List[PyObjectId]] = []
    CurrentPeriod: Optional[PyObjectId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def generate_matchups(self, period: Period) -> List[Tuple[PyObjectId, PyObjectId]]:
        teams = self.Teams[:]
        random.shuffle(teams)
        matchups = []

        # Dictionary to store past opponents for each team
        past_opponents = {team: set() for team in teams}

        # Populate past opponents from previous periods
        previous_periods = db.periods.find({"LeagueId": self.id, "PeriodNumber": {"$lt": period.PeriodNumber}})
        for prev_period in previous_periods:
            team_results = db.teamresults.find({"PeriodId": prev_period["_id"]})
            for result in team_results:
                team_id = result["TeamId"]
                opponent_id = result["OpponentId"]
                if opponent_id:
                    past_opponents[team_id].add(opponent_id)
                    past_opponents[opponent_id].add(team_id)

        # Create matchups ensuring no repeat until everyone has played each other
        while teams:
            team1 = teams.pop()
            possible_opponents = [t for t in teams if t not in past_opponents[team1]]
            
            if not possible_opponents:
                # All teams have played each other, reset past_opponents for new matchups
                matchups.append((team1, teams.pop()))
            else:
                team2 = random.choice(possible_opponents)
                teams.remove(team2)
                matchups.append((team1, team2))
                past_opponents[team1].add(team2)
                past_opponents[team2].add(team1)

        return matchups

    def create_initial_teams(self) -> bool:
        num_of_teams = self.LeagueSettings["NumOfTeams"]
        team_ids = []
        for i in range(num_of_teams):
            team = Team(
                TeamName=f"Team {i+1}",
                ProfilePicture="",
                Golfers=[],
                OwnerId=None,
                LeagueId=self.id,
                DraftPicks={},
                Points=0,
                FAAB=0,
                WaiverNumber=0
            )
            team.save()
            team_ids.append(team.id)
        
        self.Teams = team_ids
        self.CurrentStandings = team_ids
        self.save()
        return True

    def create_periods_between_tournaments(self):
        # Fetch all selected tournaments for the league
        league_settings = self.LeagueSettings
        if not league_settings or not league_settings.get("Tournaments"):
            raise ValueError("No tournaments found for this league.")

        tournament_ids = league_settings["Tournaments"]
        tournaments = list(db.tournaments.find({"_id": {"$in": tournament_ids}}).sort("StartDate"))

        if not tournaments or len(tournaments) < 2:
            raise ValueError("Insufficient tournaments to create periods.")

        # Determine draft frequency
        draft_frequency = league_settings.get("DraftFrequency")
        draft_periods = set(range(1, len(tournaments) + 1, draft_frequency))

        self.create_initial_period()

        # Create periods between consecutive tournaments
        for i in range(len(tournaments) - 1):
            current_tournament = tournaments[i]
            next_tournament = tournaments[i + 1]

            period = Period(
                LeagueId=self.id,
                StartDate=current_tournament["EndDate"],
                EndDate=next_tournament["StartDate"],
                PeriodNumber=i + 1,
                TournamentId=current_tournament["_id"],
                SeasonId=league_settings["SeasonId"]
            )

            if (i + 1) in draft_periods:
                draft = Draft(
                    LeagueId=self.id,
                    StartDate=current_tournament["EndDate"],
                    Rounds=league_settings.get("DraftRounds", 1),
                    PeriodId=period.id
                )
                draft.save()
                period.DraftId = draft.id

            period.save()

            # Create Team Results and generate matchups for head-to-head leagues
            if league_settings.get("HeadToHead"):
                matchups = self.generate_matchups(period)

                for team1_id, team2_id in matchups:
                    team1_result = TeamResult(
                        TeamId=team1_id,
                        LeagueId=self.id,
                        TournamentId=current_tournament["_id"],
                        PeriodId=period.id,
                        TotalPoints=0,
                        GolfersScores={},
                        Placing=0,
                        PointsFromPlacing=0,
                        OpponentId=team2_id
                    )
                    team2_result = TeamResult(
                        TeamId=team2_id,
                        LeagueId=self.id,
                        TournamentId=current_tournament["_id"],
                        PeriodId=period.id,
                        TotalPoints=0,
                        GolfersScores={},
                        Placing=0,
                        PointsFromPlacing=0,
                        OpponentId=team1_id
                    )
                    team1_result.save()
                    team2_result.save()

            self.save()

    def get_most_recent_season(self) -> Season:
        current_date = datetime.utcnow()
        season = db.seasons.find_one(
            {"LeagueId": self.id, "StartDate": {"$gt": current_date}},
            sort=[("StartDate", -1)]
        )
        return Season(**season) if season else None

    def get_most_recent_period(self):
        current_date = datetime.utcnow()
        period = db.periods.find_one(
            {"LeagueId": self.id, "EndDate": {"$lt": current_date}},
            sort=[("EndDate", -1)]
        )
        return Period(**period) if period else None

    def determine_waiver_order(self) -> bool:
        # Retrieve league settings
        league_settings = self.LeagueSettings

        # Check if waiver type is "Reverse Standings"
        if league_settings and league_settings.get("WaiverType") == "Reverse Standings":
            # Get the most recent period
            most_recent_period = self.get_most_recent_period()

            # Ensure the most recent period and its standings exist
            if most_recent_period and most_recent_period.Standings:
                standings = most_recent_period.Standings
                self.WaiverOrder = standings[::-1]  # Reverse the standings

                # Update WaiverNumber for each team
                for i, team_id in enumerate(self.WaiverOrder):
                    db.teams.update_one(
                        {"_id": team_id},
                        {"$set": {"WaiverNumber": i + 1}}
                    )
                return True

        return False

    def create_initial_period(self):
        # Create the initial period for the league
        first_tournament = db.tournaments.find_one({}, sort=[("StartDate", 1)])
        league_settings = self.LeagueSettings

        if not first_tournament:
            raise ValueError("No tournaments found to initialize the period.")

        # Create an initial period before the first tournament
        initial_period = Period(
            LeagueId=self.id,
            StartDate=datetime.utcnow(),
            EndDate=first_tournament["EndDate"],
            PeriodNumber=0,
            SeasonId=first_tournament["SeasonId"]
        )

        # Create the first draft before the first tournament
        first_draft = Draft(
            LeagueId=self.id,
            StartDate=datetime.utcnow(),
            Rounds=league_settings.get("DraftRounds", 1),
            PeriodId=initial_period.id
        )
        first_draft.save()
        initial_period.DraftId = first_draft.id
        initial_period.save()

    def start_new_period(self, last_tournament_end_date: datetime):
        # Create a new period starting from the end of the last tournament
        current_period_number = db.periods.count_documents({"LeagueId": self.id})

        period = Period(
            LeagueId=self.id,
            StartDate=last_tournament_end_date,
            EndDate=None,  # Will be set when the next tournament is known
            PeriodNumber=current_period_number + 1
        )
        period.save()
        self.CurrentPeriod = period.id
        self.save()

    def update_period_end_date(self, tournament_end_date: datetime):
        # Update the end date of the current period when a tournament ends
        if self.CurrentPeriod:
            period = db.periods.find_one({"_id": self.CurrentPeriod})
            if period:
                period["EndDate"] = tournament_end_date
                db.periods.update_one({"_id": self.CurrentPeriod}, {"$set": {"EndDate": tournament_end_date}})

    def handle_tournament_end(self, tournament_end_date: datetime):
        # Called when a tournament ends to update the current period and start a new one
        self.start_new_period(tournament_end_date)
            
    def update_standings(self):
        standings = []
        for team_id in self.Teams:
            team = db.teams.find_one({ "_id": team_id })
            if team:
                standings.append((team_id, team['Points']))
        # Sort teams by points
        standings.sort(key=lambda x: x[1], reverse=True)
        self.CurrentStandings = [team_id for team_id, points in standings]
        self.save()

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        league_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in league_dict and league_dict['_id'] is not None:
            # Update existing document
            result = db.leagues.update_one({'_id': league_dict['_id']}, {'$set': league_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(league_dict['_id']))
        else:
            # Insert new document
            result = db.leagues.insert_one(league_dict, session)
            self.id = result.inserted_id
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

class TeamResult(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    TeamId: PyObjectId
    LeagueId: PyObjectId
    TournamentId: PyObjectId
    PeriodId: PyObjectId
    TotalPoints: int = 0
    GolfersScores: Dict[PyObjectId, Dict[str, int]]
    Placing: Optional[int] = 0
    PointsFromPlacing: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        team_result_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in team_result_dict and team_result_dict['_id'] is not None:
            # Update existing document
            result = db.teamresults.update_one({'_id': team_result_dict['_id']}, {'$set': team_result_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(team_result_dict['_id']))
        else:
            # Insert new document
            result = db.teamresults.insert_one(team_result_dict, session)
            self.id = result.inserted_id
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
    PeriodId: PyObjectId
    Picks: List[PyObjectId]
    DraftOrder: List[PyObjectId]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        draft_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in draft_dict and draft_dict['_id'] is not None:
            # Update existing document
            result = db.drafts.update_one({'_id': draft_dict['_id']}, {'$set': draft_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(draft_dict['_id']))
        else:
            # Insert new document
            result = db.drafts.insert_one(draft_dict, session)
            self.id = result.inserted_id
        return self.id

    def determine_draft_order(self):
        # Find the league document
        league = db.leagues.find_one({"_id": self.LeagueId})
        
        if not league:
            raise ValueError("League not found")

        league = League(**league)

        # Access the latest season
        latest_season = league.get_more_recent_season()
        
        if not latest_season:
            raise ValueError("Latest season not found")

        if not latest_season['Active']:
            raise ValueError("Season is not active")

        # Check if this is the first draft of the season
        draft_count = db.drafts.count_documents({"SeasonId": self.LeagueId})
        
        if draft_count == 0:
            # Randomly generate draft order
            teams = list(db.teams.find({"LeagueId": self.LeagueId}))
            self.DraftOrder = [team['_id'] for team in teams]
            random.shuffle(self.DraftOrder)
        else:
            # Get the most recent period
            most_recent_period = self.get_most_recent_period()
            
            # if there is a most recent period and that period has standings
            # set the draft to be the reverse of the standings
            if most_recent_period and most_recent_period.Standings:
                self.DraftOrder = most_recent_period.Standings[::-1]
            else:
                raise ValueError("Most recent period or standings not found")
        
        # Update the draft order in the database
        db.drafts.update_one(
            {"SeasonId": self.LeagueId},
            {"$set": {"DraftOrder": self.DraftOrder}},
            upsert=True
        )


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

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        draft_picks_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in draft_picks_dict and draft_picks_dict['_id'] is not None:
            # Update existing document
            result = db.draftpicks.update_one({'_id': draft_picks_dict['_id']}, {'$set': draft_picks_dict}, session)
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(draft_picks_dict['_id']))
        else:
            # Insert new document
            result = db.draftpicks.insert_one(draft_picks_dict, session)
            self.id = result.inserted_id
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

