from typing import List, Optional, Tuple, Dict
from pydantic import BaseModel, Field, EmailStr, root_validator, model_validator, field_validator
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from pymongo.client_session import ClientSession
import random
import pytz

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

def get_day_number(day_name: str) -> int:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days.index(day_name)

def convert_utc_to_local(utc_dt, user_tz):
    local_tz = pytz.timezone(user_tz)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_dt

class Hole(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    Strokes: Optional[int]
    Par: Optional[bool]
    NetScore: Optional[int]
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
            result = db.holes.update_one({'_id': hole_dict['_id']}, {'$set': hole_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(hole_dict['_id']))
        else:
            # Insert new document
            result = db.holes.insert_one(hole_dict)
            self.id = result.inserted_id
        return self.id

    @field_validator('Strokes')
    def strokes_must_be_positive(cls, v):
        if v == None:
            return v
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

    def save(self) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        round_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in round_dict and round_dict['_id'] is not None:
            # Update existing document
            result = db.rounds.update_one(
                {'_id': round_dict['_id']}, {'$set': round_dict}
            )
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(round_dict['_id']))
        else:
            # Insert new document
            result = db.rounds.insert_one(round_dict)
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
            result = db.golfertournamentdetails.update_one({'_id': golfer_tournament_details_dict['_id']}, {'$set': golfer_tournament_details_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(golfer_tournament_details_dict['_id']))
        else:
            # Insert new document
            result = db.golfertournamentdetails.insert_one(golfer_tournament_details_dict)
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
    ProSeason: Optional[PyObjectId]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
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
            result = db.golfers.update_one({'_id': golfer_dict['_id']}, {'$set': golfer_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(golfer_dict['_id']))
        else:
            # Insert new document
            result = db.golfers.insert_one(golfer_dict)
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

    def save(self) -> Optional[ObjectId]:
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
    def validate_username_existence(cls, v):
        # Query the collection to find if any document has a "User" field equal to the provided value
        if db.users.find_one({"User": v}):
            raise ValueError(f"Username '{v}' is already taken.")
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
        if db.users.find_one({"Email": v}):
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
    FantasyLeagueSeasonId: PyObjectId
    Standings: Optional[List[PyObjectId]] = []                                        
    FreeAgentSignings: Optional[Dict[str, List[PyObjectId]]] = {}
    Matchups: Optional[List[Dict[PyObjectId, PyObjectId]]] = []
    Drops: Optional[Dict[PyObjectId, List]] = {}
    TournamentId: PyObjectId
    TeamResults: Optional[List[PyObjectId]] = []
    LeagueId: PyObjectId
    DraftId: Optional[PyObjectId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def determine_reverse_standings_winners(self):
        for golfer_id, waivers in self.WaiverPool.items():
            sorted_waiver_numbers = sorted(waivers, key=lambda x: list(x.values())[0])
            for entry in sorted_waiver_numbers:
                winner_id = list(entry.keys())[0]
                team = db.teams.find_one({"OwnerId": winner_id, "LeagueId": self.LeagueId})
                if len(team["Golfers"]) < team["MaxGolfersPerTeam"]:
                    team["Golfers"].append(golfer_id)
                    db.teams.update_one({"_id": team["_id"]}, {"$set": {"Golfers": team["Golfers"]}})
                    break
                else:
                    raise ValueError("There is not enough space on this team to add this golfer. Please remove a golfer.")

    def determine_faab_winners(self):
        for golfer_id, bids in self.WaiverPool.items():
            sorted_bids = sorted(bids, key=lambda x: list(x.values())[0], reverse=True)
            winner_entry = sorted_bids[0]
            winner_id = list(winner_entry.keys())[0]
            winner_bid = list(winner_entry.values())[0]

            team = db.teams.find_one({"OwnerId": winner_id, "LeagueId": self.LeagueId})
            team["Golfers"].append(golfer_id)
            team["FAAB"] -= winner_bid

            db.teams.update_one({"_id": team["_id"]}, {"$set": {"Golfers": team["Golfers"], "FAAB": team["FAAB"]}})

    def determine_waiver_winners(self) -> None:
        league = db.leagues.find_one({"_id": self.LeagueId})
        league_settings = league["LeagueSettings"]

        league_timezone = league_settings.TimeZone
        
        utc_now = datetime.now(timezone.utc)
        local_now = convert_utc_to_local(utc_now, league_timezone)
        today_day_number = local_now.weekday()
        
        waiver_day_number = get_day_number(league_settings.WaiverDeadline)

        if today_day_number <= waiver_day_number:
            raise ValueError("The waiver deadline has not passed yet.")
        
        if league_settings.WaiverType == "FAAB":
            self.determine_faab_winners()
        elif league_settings.WaiverType == "Reverse Standings":
            self.determine_reverse_standings_winners()
        else:
            raise ValueError("Invalid waiver type specified in league settings.")

    def add_to_waiver_pool(self, golfer_id: PyObjectId, user_id: PyObjectId, bid: int) -> bool:
        # Fetch the league and its settings
        league = db.leagues.find_one({"_id": self.LeagueId})
        league_settings = league["LeagueSettings"]
        team = db.teams.find_one({"OwnerId": user_id, "LeagueId": self.LeagueId})

        league_timezone = league_settings.TimeZone
        
        # Convert current UTC time to user's local time
        utc_now = datetime.now(timezone.utc)
        local_now = convert_utc_to_local(utc_now, league_timezone)
        today_day_number = get_day_number(local_now.weekday())
        
        waiver_day_number = get_day_number(league_settings.WaiverDeadline)

        if today_day_number > waiver_day_number:
            raise ValueError("The waiver deadline has passed.")

        # Check if the golfer exists
        check_golfer_in_db = db.golfers.find_one({"_id": golfer_id})
        if not check_golfer_in_db:
            raise ValueError("Sorry, that golfer does not exist.")

        # Add or update the waiver pool based on waiver type
        if golfer_id not in self.WaiverPool:
            self.WaiverPool[golfer_id] = []

        if league_settings.WaiverType == "FAAB":
            existing_entry = next((entry for entry in self.WaiverPool[golfer_id] if user_id in entry), None)
            if existing_entry:
                existing_entry[user_id] = bid
            else:
                self.WaiverPool[golfer_id].append({user_id: bid})
        elif league_settings.WaiverType == "Reverse Standings":
            if user_id not in (entry.keys() for entry in self.WaiverPool[golfer_id]):
                self.WaiverPool[golfer_id].append({user_id: team["WaiverNumber"]})
                league = League(**league)
                league.determine_waiver_order()
        else:
            raise ValueError("Invalid waiver type specified in league settings.")

        # Save the updated waiver pool
        self.save()
        return True

    def save(self) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        period_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in period_dict and period_dict['_id'] is not None:
            # Update existing document
            result = db.periods.update_one({'_id': period_dict['_id']}, {'$set': period_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(v['_id']))
        else:
            # Insert new document
            result = db.periods.insert_one(period_dict)
            self.id = result.inserted_id
        return self.id

    def set_standings(self) -> bool:
        league_id = self.LeagueId
        league_settings = db.leaguessettings.find_one({"LeagueId": league_id})

        if league_settings.HeadToHead:
            return False

        team_results = []
        
        for team_result_id in self.TeamResults:
            team_result_doc = db.teamresults.find_one({"_id": team_result_id})
            if team_result_doc:
                team_results.append(TeamResult(**team_result_doc))

        if team_results:
            if league_settings is None:
                raise ValueError("League settings not found.")

            sorted_team_results = sorted(team_results, key=lambda x: x.TeamScore, reverse=True)

            for placing, team_result in enumerate(sorted_team_results, start=1):
                points_from_placing = 0

                points_per_placing_arr = league_settings.PointsPerPlacing
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

    @model_validator(mode='before')
    def validate_dates(cls, values):
        start_date = values.get('StartDate')
        end_date = values.get('EndDate')
        today = datetime.now()

        # Check if the start date is before today's date
        if start_date and start_date < today:
            raise ValueError('Start date cannot be before today\'s date')

        # Check if end date is after start date
        if start_date and end_date and end_date <= start_date:
            raise ValueError('End date must be after start date')

        return values

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

        if league_settings.HeadToHead:
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

                points_per_placing_arr = league_settings.PointsPerPlacing

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

class ProSeason(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    LeagueName: str
    StartDate: datetime
    EndDate: datetime
    Competitions: List[PyObjectId] = []
    Active: bool = Field(default=False, description="Determine whether the season is currently active")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> PyObjectId:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        season_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in season_dict and season_dict['_id'] is not None:
            result = db.proSeasons.update_one({'_id': season_dict['_id']}, {'$set': season_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(season_dict['_id']))
        else:
            result = db.proSeasons.insert_one(season_dict)
            self.id = result.inserted_id

        return self.id

class FantasyLeagueSeason(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    SeasonNumber: int
    StartDate: datetime
    EndDate: datetime
    Periods: Optional[List[PyObjectId]] = []
    CurrentPeriod: Optional[PyObjectId] = None
    Tournaments: List[PyObjectId] = []
    LeagueId: PyObjectId
    Active: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")
    Winner: PyObjectId = Field(default=None, description="Winner user ObjectId of the league")
    CurrentStandings: List[PyObjectId] = Field(default=[], description="Array of teams sorted by the number of points they have or wins and losses.")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def start_new_period(self):
        # Create a new period starting from the end of the last tournament
        current_period = db.periods.find_one({ "_id": self.CurrentPeriod })

        next_period = db.periods.find_one({ "PeriodNumber": current_period["PeriodNumber"] + 1 })

        self.CurrentPeriod = next_period.id
        self.save()

    def update_period_end_date(self, tournament_end_date: datetime):
        # Update the end date of the current period when a tournament ends
        if self.CurrentPeriod:
            period = db.periods.find_one({"_id": self.CurrentPeriod})
            if period:
                period["EndDate"] = tournament_end_date
                db.periods.update_one({"_id": self.CurrentPeriod}, {"$set": {"EndDate": tournament_end_date}})

    def update_standings(self):
        league = db.leagues.find_one({
            "_id": self.LeagueId
        })

        standings = []
        for team_id in league.Teams:
            team = db.teams.find_one({ "_id": team_id })
            if team:
                standings.append((team_id, team['Points']))
        # Sort teams by points
        standings = standings.sort(key=lambda x: x[1], reverse=True)
        self.CurrentStandings = [team_id for team_id, points in standings]
        self.save()

    def save(self) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        fantasy_league_season_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in fantasy_league_season_dict and fantasy_league_season_dict['_id'] is not None:
            # Update existing document
            result = db.fantasyLeagueSeasons.update_one({'_id': fantasy_league_season_dict['_id']}, {'$set': fantasy_league_season_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(fantasy_league_season_dict['_id']))
        else:
            # Insert new document
            result = db.fantasyLeagueSeasons.insert_one(fantasy_league_season_dict)
            self.id = result.inserted_id
        return self.id

    @field_validator('Tournaments')
    def validate_tournament_start_dates(cls, tournament_ids_list):
        current_date = datetime.now()

        # Query the database for tournaments with the specified IDs
        tournaments = db.tournaments.find({
            "_id": {"$in": tournament_ids_list}
        })

        # Check if any tournament's start date is before today's date
        for tournament in tournaments:
            if "StartDate" in tournament and tournament["StartDate"] < current_date:
                raise ValueError(f"Tournament {tournament['_id']} has a start date before today.")

        return tournament_ids_list

    
    @model_validator(mode='before')
    def validate_and_convert_dates(cls, values):
        start_date = values.get('StartDate')
        end_date = values.get('EndDate')

        if isinstance(start_date, str):
            values['StartDate'] = datetime.fromisoformat(start_date)
        
        if isinstance(end_date, str):
            values['EndDate'] = datetime.fromisoformat(end_date)
        
        return values

    @field_validator('StartDate', 'EndDate')
    def dates_must_be_valid(cls, v, field):
        if not isinstance(v, datetime):
            raise ValueError(f'{field.name} must be a datetime')
        return v

    @model_validator(mode='before')
    def validate_dates(cls, values):
        start_date = values.get('StartDate')
        end_date = values.get('EndDate')

        if start_date and end_date and end_date <= start_date:
            raise ValueError('End date must be after start date')

        return values

class LeagueSettings(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    created_at: Optional[datetime] = None
    CutPenalty: int = Field(default=0, description="Default points for players finishing outside the defined placements")
    DraftingFrequency: int = Field(default=0, description="The number of times the league drafts in between tournaments.")
    DraftStartDayOfWeek: Optional[str] = Field(default="Monday", description="Day of the week in which the draft starts before a tournament or season.")
    DraftStartTime: Optional[str] = Field(default="12:00", description="Time of day when the draft starts, in HH:MM format.")
    DropDeadline: Optional[str] = None
    ForceDrops: Optional[int] = 0
    HeadToHead: bool = Field(default=False, description="Determine whether the competition is league wide or just between two users for each week.")
    LeagueId: PyObjectId
    MaxDraftedPlayers: int = Field(default=1, ge=0, description="Number of draft players per period")
    MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
    MaxNumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
    MinFreeAgentDraftRounds: int = Field(default=3, ge=1, description="Minimum number of draft rounds that need to be created each period")
    NumOfBenchGolfers: int = Field(default=1, ge=1, description="Number of bench players per team")
    NumOfStarters: int = Field(default=2, ge=1, description="Number of starters per team")
    NumberOfTeams: Optional[int] = Field(default=8, description="Number of the teams within the league.")
    PointsPerPlacing: Optional[List[int]] = Field(default=[], description="Points awarded for placements")
    PointsPerScore: Optional[dict] = Field(default_factory=lambda: {
        'Birdies': 3,
        'Eagles': 5,
        'Pars': 1,
        'Albatross': 7,
        'Bogeys': -3,
        'DoubleBogeys': -5,
        'WorseThanDoubleBogeys': -7
    }, description="Points awarded per round performance")
    ScorePlay: bool = Field(default=False, description="Score will accumulate based on the particular number of strokes under par the golfer receives and how many points the league agrees that type of score should receive.")
    SecondsPerDraftPick: Optional[int] = Field(default=3600, description="Time to draft in seconds, default is 3600 seconds (1 hour)")
    SnakeDraft: bool = Field(default=True, description="The order of picks reverses with each round.")
    StrokePlay: bool = Field(default=False, description="Score will match the under par score for the golfer in the tournament")
    TimeZone: str = "UTC"
    updated_at: Optional[datetime] = None
    WaiverDeadline: Optional[str] = Field(default="Wednesday", description="Day of the week where players on waivers are distributed.")
    WaiverType: str = Field(default="Reverse Standings", description="Determine the priority with which teams receive in picking up free agents")

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

    def save(self, league_id: Optional[PyObjectId] = None) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        league_settings_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in league_settings_dict and league_settings_dict['_id'] is not None:
            # Update existing document
            result = db.leagueSettings.update_one({'_id': league_settings_dict['_id']}, {'$set': league_settings_dict})

            # If league_id is provided, associate the new LeagueSettings with the League
            if league_id is not None:
                db.leagues.update_one({'_id': league_id}, {'$set': {'LeagueSettings': league_settings_dict}})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(league_settings_dict['_id']))
        else:
            # Insert new document
            result = db.leagueSettings.insert_one(league_settings_dict)
            self.id = result.inserted_id
            # If league_id is provided, associate the new LeagueSettings with the League
            if league_id is not None:
                db.leagues.update_one({'_id': league_id}, {'$set': {'LeagueSettings': league_settings_dict}})

        return self.id

    @field_validator('DraftStartTime')
    def validate_draft_start_time(cls, v):
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('DraftStartTime must be in HH:MM format')
        hours, minutes = map(int, v.split(':'))
        if not (0 <= hours < 24) or not (0 <= minutes < 60):
            raise ValueError('DraftStartTime must be a valid time in HH:MM format')
        return v

    # only matters if the league is running head to head matchups
    @model_validator(mode='before')
    def validate_number_of_teams(cls, values):
        number_of_teams = values.get('NumberOfTeams')
        head_to_head = values.get('HeadToHead')
        print(head_to_head, number_of_teams)

        if head_to_head and number_of_teams % 2 != 0:
            print("After validation")
            raise ValueError("The number of teams in your league must be even if you want to play a head-to-head league.")

        return values

    @field_validator('NumberOfTeams')
    def num_of_teams_constraint(cls, v):
        print(v)
        if v > 16:
            raise ValueError("There cannot be more than 16 teams in a league.")
        return v

    @model_validator(mode='before')
    def validate_draft_rounds(cls, values):
        min_free_agent_draft_rounds = values.get('MinFreeAgentDraftRounds')
        max_golfers_per_team = values.get('MaxGolfersPerTeam')

        if max_golfers_per_team is not None and min_free_agent_draft_rounds >= max_golfers_per_team:
            raise ValueError('The amount of draft rounds that have been created is more than the max amount of players allowed per team.')
        
        return values

    @field_validator('SecondsPerDraftPick')
    def time_to_draft_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Time to draft must be a positive period of time.')
        return v

    @model_validator(mode='before')
    def validate_num_of_starters(cls, values):
        num_of_starters = values.get('NumOfStarters')
        max_golfers_per_team = values.get('MaxGolfersPerTeam')

        if max_golfers_per_team is not None and num_of_starters >= max_golfers_per_team:
            raise ValueError('Number of defined players must be less than the maximum number of golfers per team.')

        return values

    @model_validator(mode='before')
    def validate_max_drafted_players(cls, values):
        max_drafted_players = values.get('MaxDraftedPlayers')
        max_golfers_per_team = values.get('MaxGolfersPerTeam')

        if max_drafted_players is not None and max_golfers_per_team is not None:
            if max_drafted_players > max_golfers_per_team:
                raise ValueError("Max draftable players must be less than or equal to the maximum golfers allowed on a team.")
        
        return values

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

    @field_validator('WaiverType')
    def define_waiver_fomat(cls, v):
        if v not in ["Reverse Standings", "Bidding"]:
            raise ValueError("Waiver type must be either a bidding format or first to last.")
        return v

    @model_validator(mode = 'before')
    def bench_players_under_limit(cls, values):
        num_of_bench_golfers = values.get('NumOfBenchGolfers')
        max_golfers_per_team = values.get('MaxGolfersPerTeam')
        num_of_starters = values.get('NumOfStarters')

        if num_of_bench_golfers > max_golfers_per_team or num_of_bench_golfers > num_of_starters // 2:
            return ValueError("Your number of bench golfers must be less than half your starters count and less than max amount of players allowed on a team.")
        return values

    def drafting_period_must_be_valid(self):
        league = db.leagues.find_one({ "_id": self.LeagueId })
        season = db.fantasyLeagueSeasons.find_one({ "_id": league["CurrentFantasyLeagueSeasonId"], "LeagueId": league["_id"]})
        if self.DraftingFrequency > len(season["Tournaments"]):
            raise ValueError("You cannot have more drafts than you have selected tournaments")
        return True

    def __init__(self, **data):
        super().__init__(**data)
        self.determine_points_per_placing()

class Team(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    TeamName: str
    ProfilePicture: Optional[str] = Field(description="Profile picture for team")
    Golfers: Dict[str, Dict[str, any]] = Field(default_factory=dict, description="Dictionary of golfer IDs with usage count and team status")
    OwnerId: Optional[PyObjectId] = None
    LeagueId: PyObjectId
    Points: int = Field(default=0, description="the amount of points that the team holds for the season based on their aggregate fantasy placings")
    FAAB: int = Field(default=0, description="How much total points you have to spend on players.")
    WaiverNumber: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Validation to ensure the length of TeamName and LeagueName is reasonable
    @field_validator('TeamName')
    def validate_name_length(cls, v):
        if len(v) < 3 or len(v) > 50:  
            # Example: setting reasonable length between 3 and 50 characters
            raise ValueError('Name must be between 3 and 50 characters long.')
        return v

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    def change_team_name(old_team_name: str, new_team_name: str, league_id: PyObjectId):
        # Find the team document in the database
        team = db.teams.find_one({
            "TeamName": old_team_name,
            "LeagueId": league_id
        })

        # Raise an error if the team is not found
        if not team:
            raise ValueError("Sorry, we could not find the team you are looking for.")

        # Raise an error if the new name is not provided
        if not new_team_name:
            raise ValueError("Please enter a new team name.")

        # Update the team name in the retrieved document
        team["TeamName"] = new_team_name

        # Create a new instance of Team for validation
        new_team = Team(**team)

        # Save the new instance to the database
        new_team.save()

    def drop_player(self, team_id: PyObjectId, golfer_id: PyObjectId) -> bool:
        # Find the team
        team = db.teams.find_one({"_id": team_id})

        if not team:
            raise ValueError("The team you entered does not exist.")

        if golfer_id not in team["Golfers"]:
            raise ValueError(f"Player with ID {golfer_id} is not on the team.")
        else:
            # Update the team by removing the golfer
            db.teams.update_one(
                {"_id": team_id},
                {"$pull": {"Golfers": golfer_id}}
            )
            
            # Update the period's drop list
            league = db.leagues.find_one({"_id": self.LeagueId})
            if league:
                current_period = db.periods.find_one({"LeagueId": self.LeagueId, "StartDate": {"$lte": datetime.utcnow()}, "EndDate": {"$gte": datetime.utcnow()}})
                if current_period:
                    period_id = current_period["_id"]
                    drops = current_period.get("Drops", {})

                    if team_id in drops:
                        drops[team_id].append(golfer_id)
                    else:
                        drops[team_id] = [golfer_id]

                    db.periods.update_one(
                        {"_id": period_id},
                        {"$set": {"Drops": drops}}
                    )
                else:
                    raise ValueError("No current period found for the league.")
        
        return True

    def save(self) -> Optional[ObjectId]:
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
            self.id = result.inserted_id
        return self.id

    def sign_free_agent(self, free_agent_id: str, period_id: PyObjectId):
        # FreeAgentSignings: Optional[Dict[str, List]] = []

        current_period = db.periods.find_one({
            "_id": period_id
        })

        if not current_period:
            raise ValueError("Period does not exist. Please check the ID you entered and try again.")

        # Check if the team's ID already exists in the FreeAgentSignings
        if self.id in current_period["FreeAgentSignings"]:
            # Add the new signing details to the existing list for this team
            db.periods.update_one(
                {"_id": current_period["_id"]},
                {"$push": {f"FreeAgentSignings.{self.id}": free_agent_id}}
            )
        else:
            # If the team ID does not exist, initialize it with a new list containing the new signing
            db.periods.update_one(
                {"_id": current_period["_id"]},
                {"$set": {f"FreeAgentSignings.{self.id}": [free_agent_id]}}
            )

        self.add_to_golfer_usage(free_agent_id)

    def add_to_golfer_usage(self, golfer_id: str, bench: bool = False):
        golfer_id_str = str(golfer_id)

        # find the leagueSettings
        league_settings = db.leagueSettings.find_one({
            "LeagueId": self.LeagueId 
        })

        # Count the number of current golfers on the team
        num_of_golfers = len([g for g in self.Golfers.keys() if self.Golfers[g].get('CurrentlyOnTeam', True)])

        if num_of_golfers > league_settings["MaxGolfersPerTeam"]:
            raise ValueError("You have reached the maximum allowable golfers per team.")

        # Count the number of current starters
        num_of_starters = len([g for g in self.Golfers.keys() if self.Golfers[g].get('IsStarter', True)])

        if golfer_id_str in self.Golfers:
            self.Golfers[golfer_id_str]['UsageCount'] += 1
            if bench:
                self.Golfers[golfer_id_str]['IsBench'] = True
                self.Golfers[golfer_id_str]['IsStarter'] = False
        else:
            if num_of_starters >= league_settings['NumOfStarters'] or bench:
                self.Golfers[golfer_id_str] = { 'UsageCount': 1, 'CurrentlyOnTeam': True, 'IsStarter': False, 'IsBench': True }
            else:
                self.Golfers[golfer_id_str] = { 'UsageCount': 1, 'CurrentlyOnTeam': True, 'IsStarter': True, 'IsBench': False }

        self.save()

    def remove_golfer(self, golfer_id: str):
        golfer_id = str(golfer_id)

        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['CurrentlyOnTeam'] = False
            self.Golfers[golfer_id]['IsStarter'] = False
            self.Golfers[golfer_id]['IsBench'] = False
        else:
            print(f"Golfer ID {golfer_id} not found on this team.")

        self.save()

    def get_golfer_usage(self, golfer_id: PyObjectId) -> int:
        return self.Golfers.get(golfer_id, {}).get('UsageCount', 0)

    def is_golfer_on_team(self, golfer_id: PyObjectId) -> bool:
        return self.Golfers.get(golfer_id, {}).get('CurrentlyOnTeam', False)

    def set_golfer_as_starter(self, golfer_id: PyObjectId):
        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['IsStarter'] = True
            self.Golfers[golfer_id]['IsBench'] = False
        self.save()

    def set_golfer_as_bench(self, golfer_id: str):
        golfer_id = str(golfer_id)
    
        if golfer_id in self.Golfers:
            self.Golfers[golfer_id]['IsStarter'] = False
            self.Golfers[golfer_id]['IsBench'] = True
        self.save()

    def total_golfers(self) -> int:
        return sum(1 for golfer in self.Golfers.values() if golfer['CurrentlyOnTeam'])

    def get_all_current_golfers_ids(self) -> int:
        # Collect all golfer IDs that are currently on the team
        golfer_ids = [golfer_id for golfer_id in self.Golfers.keys() if self.Golfers[golfer_id]['CurrentlyOnTeam']]
        
        return golfer_ids

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
    CommissionerId: PyObjectId
    Teams: List[PyObjectId] = []
    LeagueSettings: Optional[LeagueSettings]
    FantasyLeagueSeasons: Optional[List[PyObjectId]] = []
    CurrentFantasyLeagueSeasonId: Optional[PyObjectId] = None
    WaiverOrder: Optional[List[PyObjectId]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Validation to ensure the length of TeamName and LeagueName is reasonable
    @field_validator('Name')
    def validate_name_length(cls, v):
        if len(v) < 3 or len(v) > 50:  
            # Example: setting reasonable length between 3 and 50 characters
            raise ValueError('Name must be between 3 and 50 characters long.')
        return v

    def find_current_season(self) -> Optional[FantasyLeagueSeason]:
        if self.CurrentFantasyLeagueSeason:
            current_season = db.fantasyLeagueSeasons.find_one({"_id": self.CurrentFantasyLeagueSeason})
            if current_season:
                return FantasyLeagueSeason(**current_season)
        return None

    def determine_current_fantasy_league_season(self) -> Optional[ObjectId]:
        current_date = datetime.now()

        for season_id in self.FantasyLeagueSeasons:
            # Assuming you have a way to get a FantasyLeagueSeason by its ID
            season = db.fantasyleagueseasons.find_one({"_id": season_id})

            if season:
                start_date = season.get("startdate")
                end_date = season.get("enddate")

                if start_date <= current_date <= end_date:
                    # Update the league with the current FantasyLeagueSeasonId
                    db.leagues.update_one(
                        {"_id": self.id},
                        {"$set": {"CurrentFantasyLeagueSeasonId": season_id}}
                    )
                    return season_id

        # If no current season is found, you may want to clear the current season
        db.leagues.update_one(
            {"_id": self.id},
            {"$set": {"CurrentFantasyLeagueSeasonId": None}}
        )
        return None

    def convert_to_datetime(self, day_of_week: str, time_str: str, timezone_str: str) -> datetime:
        day_number = get_day_number(day_of_week)
        time_parts = time_str.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        now = datetime.now(pytz.timezone(timezone_str))
        current_day_number = now.weekday()
        
        days_ahead = day_number - current_day_number
        if days_ahead <= 0:
            days_ahead += 7

        draft_start = now + timedelta(days=days_ahead)
        draft_start = draft_start.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return draft_start

    def create_initial_season(self, tournaments: List[Tournament]) -> PyObjectId:
        if not self.FantasyLeagueSeasons or len(self.FantasyLeagueSeasons) < 1:
            if not tournaments:
                raise ValueError("No tournaments specified for the initial season.")

            first_tournament_doc = tournaments[0]
            last_tournament_doc = tournaments[-1]

            tournament_ids = [ObjectId(tournament["_id"]) for tournament in tournaments]

            print(first_tournament_doc['StartDate'], last_tournament_doc['EndDate'])

            first_season = FantasyLeagueSeason(
                SeasonNumber=1,
                StartDate=first_tournament_doc["StartDate"],
                EndDate=last_tournament_doc["EndDate"],
                Periods=[],
                LeagueId=self.id,
                Tournaments=tournament_ids,
                Active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            first_season_id = first_season.save()
            print(first_season_id)

            self.FantasyLeagueSeasons.append(first_season_id)
            self.CurrentFantasyLeagueSeasonId = first_season_id
            self.save()

            return first_season_id

    def transition_to_next_season(self, tournaments: List[PyObjectId]) -> PyObjectId:
        current_season = self.find_current_season()
        if not current_season:
            raise ValueError("Current season not found.")

        current_season.Active = False
        current_season.save()

        if not tournaments:
            raise ValueError("No tournaments specified for the next season.")

        next_season_number = current_season.SeasonNumber + 1
        tournament_docs = list(db.tournaments.find({"_id": {"$in": tournaments}}))
        if not tournament_docs:
            raise ValueError("Could not find the specified tournaments in the database.")

        tournament_docs = sorted(tournament_docs, key=lambda x: x["StartDate"])
        first_tournament_doc = tournament_docs[0]
        last_tournament_doc = tournament_docs[-1]

        next_season = FantasyLeagueSeason(
            SeasonNumber=next_season_number,
            StartDate=first_tournament_doc["StartDate"],
            EndDate=last_tournament_doc["EndDate"],
            Periods=[],
            LeagueId=self.id,
            Tournaments=tournaments,
            Active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        next_season_id = next_season.save()

        self.FantasyLeagueSeasons.append(next_season_id)
        self.CurrentSeason = next_season_id
        self.save()

        return next_season_id

    def remove_lowest_ogwr_golfer(team_id: PyObjectId) -> PyObjectId:
        # Find the team by ID
        team = db.teams.find_one({"_id": ObjectId(team_id)})
        if not team:
            raise ValueError("Team not found.")

        # Get the list of golfer IDs
        golfer_ids = team['Golfers']
        
        # Query and sort golfers by OGWR to get the lowest one
        lowest_golfer = db.golfers.find({"_id": {"$in": golfer_ids}}).sort("OGWR", 1).limit(1)
        
        lowest_golfer = list(lowest_golfer)
        if not lowest_golfer:
            raise ValueError("No golfers found in the team.")

        # Remove the golfer with the lowest OGWR from the team
        lowest_golfer_id = lowest_golfer[0]['_id']
        
        db.teams.update_one(
            {"_id": ObjectId(team_id)},
            {"$pull": {"Golfers": lowest_golfer_id}}
        )

        return lowest_golfer_id

    def enforce_drop_deadline(self):
        if self.LeagueSettings.ForceDrops > 0:
            league_timezone = self.LeagueSettings.TimeZone
            
            # Convert current UTC time to user's local time
            utc_now = datetime.now(timezone.utc)
            local_now = convert_utc_to_local(utc_now, league_timezone)
            today_day_number = get_day_number(local_now.weekday())
            
            drop_day_number = get_day_number(self.LeagueSettings.DropDeadline)

            if today_day_number > drop_day_number:
                period = self.get_most_recent_period()
                for id in self.Teams:
                    # force drop players if the team owner has not to do so
                    # according to the league settings force drop rules
                    while period.Drops[id] < self.LeagueSettings.ForceDrops:
                        # remove the last golfer from their team
                        self.remove_lowest_ogwr_golfer(id)

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
        league_settings = self.LeagueSettings
        num_of_teams = league_settings.NumberOfTeams
        team_ids = []

        for i in range(num_of_teams):
            team = Team(
                TeamName=f"Team {i+1}",
                ProfilePicture="",
                Golfers={},
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
        # Fetch all selected tournaments for this season and league
        season_id = self.CurrentFantasyLeagueSeasonId
        if not season_id:
            raise ValueError("there is no current season ongoing for this league")

        season_doc = db.fantasyLeagueSeasons.find_one({ 
            "_id": season_id
        })

        tournament_ids = season_doc["Tournaments"]
        tournaments = list(db.tournaments.find({"_id": {"$in": tournament_ids}}).sort("StartDate"))

        if not tournaments or len(tournaments) < 2:
            raise ValueError("Insufficient tournaments to create periods.")
        
        league_settings = self.LeagueSettings

        # Determine draft frequency
        draft_frequency = league_settings.DraftingFrequency
        draft_periods = set(range(1, len(tournaments) + 1, draft_frequency))

        self.create_initial_period(season_id)

        period_ids = []

        # Create periods between consecutive tournaments
        for i in range(1, len(tournaments) - 1):
            current_tournament = tournaments[i]
            next_tournament = tournaments[i + 1]

            period = Period(
                LeagueId=self.id,
                StartDate=current_tournament["EndDate"],
                EndDate=next_tournament["StartDate"],
                PeriodNumber=i + 1,
                TournamentId=current_tournament["_id"],
                FantasyLeagueSeasonId=self.CurrentFantasyLeagueSeasonId
            )

            if (i + 1) in draft_periods:
                draft = Draft(
                    LeagueId=self.id,
                    StartDate=current_tournament["EndDate"],
                    Rounds=league_settings.MinFreeAgentDraftRounds,
                    PeriodId=period.id,
                    Picks=[],
                    DraftOrder=[]
                )
                draft.save()
                period.DraftId = draft.id

            period_id = period.save()
            period_ids.append(period_id)
            print(period_id)

            # Create Team Results and generate matchups for head-to-head leagues
            if league_settings.HeadToHead:
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
        db.fantasyLeagueSeasons.update_one(
            {"_id": self.CurrentFantasyLeagueSeasonId},  # Filter to find the document
            {"$set": {"Periods": period_ids}}       # Update operation to set the new value
        )

    def get_most_recent_season(self) -> FantasyLeagueSeason:
        current_date = datetime.utcnow()
        season = db.fantasyLeagueSeasons.find_one(
            {"LeagueId": self.id, "StartDate": {"$gt": current_date}},
            sort=[("StartDate", -1)]
        )
        return FantasyLeagueSeason(**season) if season else None

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
        if league_settings and league_settings.WaiverType == "Reverse Standings":
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

    def create_initial_period(self, season_id): 
        # Create the initial period for the league
        season = db.fantasyLeagueSeasons.find_one({
            "_id": season_id
        })
        first_tournament = season["Tournaments"][0]

        league_settings = self.LeagueSettings

        if not first_tournament:
            raise ValueError("No tournaments found to initialize the period.")

        draft_start_date = self.convert_to_datetime(
            league_settings.DraftStartDayOfWeek,
            league_settings.DraftStartTime,
            league_settings.TimeZone
        )

        # Create an initial period before the first tournament
        initial_period = Period(
            LeagueId=self.id,
            StartDate=datetime.utcnow(),
            EndDate=first_tournament["EndDate"],
            TournamentId=first_tournament["_id"],
            PeriodNumber=1,
            FantasyLeagueSeasonId=self.CurrentFantasyLeagueSeasonId
        )

        initial_period_id = initial_period.save()

        first_draft_id = self.create_initial_draft(draft_start_date, initial_period_id, league_settings.MaxGolfersPerTeam)

        initial_period.DraftId = first_draft_id

        initial_period.save()

    def create_initial_draft(self, draft_start_date, initial_period_id, max_golfers_per_team) -> PyObjectId:

        # Create the first draft before the first tournament
        first_draft = Draft(
            LeagueId=self.id,
            StartDate=draft_start_date,
            Rounds=max_golfers_per_team,
            PeriodId=initial_period_id,
            Picks=[],
            DraftOrder=[]
        )

        first_draft_id = first_draft.save()

        return first_draft_id

    def handle_tournament_end(self, tournament_end_date: datetime):
        # Called when a tournament ends to update the current period and start a new one
        self.start_new_period(tournament_end_date)

    def save(self, session: Optional[ClientSession] = None) -> Optional[ObjectId]:
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
    TournamentId: PyObjectId
    PeriodId: PyObjectId
    OpponentId: Optional[PyObjectId] = None
    TeamScore: int = 0
    GolfersScores: List[PyObjectId] = Field(default={}, description="Dictionary with a string for the golfer tourney details id as the key and ")
    Placing: Optional[int] = 0
    PointsFromPlacing: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        team_result_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in team_result_dict and team_result_dict['_id'] is not None:
            # Update existing document
            result = db.teamResults.update_one({'_id': team_result_dict['_id']}, {'$set': team_result_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(team_result_dict['_id']))
        else:
            # Insert new document
            result = db.teamResults.insert_one(team_result_dict)
            self.id = result.inserted_id
            
            # Insert id into the associated Period
            period_id = team_result_dict.get("PeriodId")
            if period_id:
                db.periods.update_one(
                    {"_id": period_id},
                    {"$push": {"TeamResults": self.id}}
                )
            else:
                raise ValueError("PeriodId is missing or invalid in team_result_dict")

        return self.id
    
    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
    
    @model_validator(mode = 'before')
    def placing_is_less_than_teams(cls, values):
        period_id = values.get('PeriodId')

        period = db.periods.find_one({ "_id": period_id })
        league_id = period["LeagueId"]

        placing = values.get('Placing')

        num_of_teams_in_league = len(db.leagues.find_one({"_id": league_id })["Teams"])
        if placing > num_of_teams_in_league:
            raise ValueError('The placing the team currently is in is not possible based on the amount of teams in the league')
        return values

    def calculate_player_scores(self, db):
        league_settings = db.leaguessettings.find_one({"LeagueId": self.LeagueId})
        
        if league_settings is None:
            raise ValueError("League settings not found.")
        
        points_per_score = league_settings.PointsPerScore
        
        for golfer_id in self.GolfersScores.items():
            golfer_details = db.golfertournamentdetails.find_one({"GolferId": golfer_id, "TournamentId": self.TournamentId})
            
            if golfer_details is None:
                continue
            
            if league_settings.StrokePlay:
                self.GolfersScores[golfer_id]['TotalScore'] = golfer_details.get('TotalScore', 0)
            elif league_settings.ScorePlay:
                for score_type in ['Birdies', 'Pars', 'Bogeys', 'DoubleBogeys', 'WorseThanDoubleBogeys']:
                    historical_num_of_score_type = self.GolfersScores[golfer_id].get(score_type, 0)
                    curr_num_of_score_type = golfer_details.get(score_type, 0)
                    if historical_num_of_score_type != curr_num_of_score_type:
                        difference_in_score_type_count = curr_num_of_score_type - historical_num_of_score_type
                        self.TotalPoints += (points_per_score.get(score_type, 0) * difference_in_score_type_count)
                        self.GolfersScores[golfer_id][score_type] = curr_num_of_score_type

class Draft(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    LeagueId: PyObjectId
    StartDate: datetime
    EndDate: Optional[datetime] = None
    Rounds: int
    PeriodId: PyObjectId
    DraftPicks: Optional[List[PyObjectId]]
    DraftOrder: Optional[List[PyObjectId]]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[ObjectId]:
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
            self.id = result.inserted_id
        return self.id

    def determine_draft_order(self):
        # Find the league document
        league = db.leagues.find_one({"_id": self.LeagueId})
        
        if not league:
            raise ValueError("League not found")

        league = League(**league)

        # Access the latest season
        latest_season = league.get_most_recent_season()

        if not latest_season['Active']:
            raise ValueError("Season is not active")

        # Check if this is the first draft of the season
        draft_count = db.drafts.count_documents({ "SeasonId": latest_season["_id"] })
        
        if draft_count == 0:
            # Randomly generate draft order
            teams = list(db.teams.find({ "LeagueId": self.LeagueId }))
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
            {"FantasyLeagueSeasonId": self.LeagueId},
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
    TeamId: PyObjectId
    GolferId: PyObjectId
    RoundNumber: int
    PickNumber: int
    LeagueId: PyObjectId
    DraftId: PyObjectId
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def save(self) -> Optional[ObjectId]:
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        draft_picks_dict = self.dict(by_alias=True, exclude_unset=True)

        if '_id' in draft_picks_dict and draft_picks_dict['_id'] is not None:
            # Update existing document
            result = db.draftPicks.update_one({'_id': draft_picks_dict['_id']}, {'$set': draft_picks_dict})
            if result.matched_count == 0:
                raise ValueError("No document found with _id: {}".format(draft_picks_dict['_id']))
        else:
            # Insert new document
            result = db.draftPicks.insert_one(draft_picks_dict)
            self.id = result.inserted_id
            
            # Append the new draft pick to the DraftPicks array in the drafts collection
            db.drafts.update_one(
                {"_id": draft_picks_dict['DraftId']},
                {"$push": {"DraftPicks": self.id}}
            )
        
        return self.id

    @root_validator(pre=True)
    def run_validations(cls, values):
        # Use the raw values dictionary for validation purposes
        league_settings = db.leagueSettings.find_one({"LeagueId": values['LeagueId']})
        if not league_settings:
            raise ValueError("League settings not found")

        team_golfers_count = db.golfers.count_documents({"TeamId": values['TeamId']})
        if team_golfers_count >= league_settings['MaxGolfersPerTeam']:
            raise ValueError("Team already has the maximum number of golfers allowed")

        draft = db.drafts.find_one({"LeagueId": values['LeagueId']})
        if not draft:
            raise ValueError("Draft not found")

        # current_time = datetime.now()
        # draft_start_time = draft['StartDate']
        # pick_duration = draft.get('TimeToDraft', 7200)
        # picks_per_round = len(draft['Picks']) / draft['Rounds']
        # expected_pick_time = draft_start_time + timedelta(
        #     seconds=(values['RoundNumber'] - 1) * picks_per_round * pick_duration +
        #             (values['PickNumber'] - 1) * pick_duration
        # )

        # if current_time < draft_start_time or current_time > expected_pick_time + timedelta(seconds=pick_duration):
        #     raise ValueError("Pick is not within the allowed time period")

        # if len(draft['Picks']) >= values['PickNumber'] + (values['RoundNumber'] - 1) * picks_per_round:
        #     raise ValueError("Invalid pick order")

        return values

    @field_validator('RoundNumber', 'PickNumber')
    def pick_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Round number and pick number must be positive')
        return v

