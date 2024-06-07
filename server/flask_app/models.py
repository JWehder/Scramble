from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator, root_validator
from datetime import datetime
from bson import ObjectId
from config import 

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


class Hole(BaseModel):
    Id: Optional[PyObjectId] = Field(alias='_id')
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
    GolferTournamentDetailsId: str
    RoundId: str

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
    Id: Optional[PyObjectId] = Field(alias='_id')
    GolferTournamentDetailsId: str
    Round: str
    Birdies: int
    Eagles: int
    Pars: int
    Albatross: int
    Bogeys: int
    DoubleBogeys: int
    WorseThanDoubleBogeys: int
    Score: int
    Holes: List[Hole]

    @validator('Score')
    def score_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Score must be positive')
        return v

class GolferTournamentDetails(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    GolferId: str
    Position: str
    Name: str
    Score: str
    R1: str
    R2: str
    R3: str
    R4: str
    TotalStrokes: str
    Earnings: str
    FedexPts: str
    TournamentId: str
    Rounds: List[PyObjectId]

class Tournament(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    end_date: datetime
    start_date: datetime
    name: str
    venue: List[str]
    city: str
    state: str
    links: List[str]
    purse: int
    previous_winner: str
    par: str
    yardage: str
    is_completed: bool
    in_progress: bool
    golfers: List[PyObjectId]

    @validator('par')
    def par_must_be_valid(cls, v):
        valid_pars = ['3', '4', '5', '6']
        if v not in valid_pars:
            raise ValueError(f'Par must be one of {valid_pars}')
        return v

class Golfer(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    rank: str
    first_name: str
    last_name: str
    age: int
    earnings: int
    fedex_pts: int
    events: int
    rounds: int
    country: str
    flag: str
    cuts: int
    top10s: int
    wins: int
    avg_score: float
    golfer_page_link: str
    birthdate: datetime
    birthplace: str
    college: str
    swing: str
    turned_pro: str
    tournament_details: List[GolferTournamentDetails]
    owgr: str

    @validator('rank', 'owgr')
    def rank_and_owgr_must_be_valid(cls, v):
        if not v.isdigit() or int(v) <= 0:
            raise ValueError('Rank and OWGR must be positive integers')
        return v

    @validator('age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be a positive integer')
        return v

    @validator('earnings', 'fedex_pts', 'events', 'rounds', 'cuts', 'top10s', 'wins')
    def must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

    @validator('avg_score')
    def avg_score_must_be_valid(cls, v):
        if v <= 0 or v > 100:
            raise ValueError('Average score must be a positive number and realistic')
        return v

    @validator('golfer_page_link')
    def must_be_valid_url(cls, v):
        if not v.startswith("http"):
            raise ValueError('Golfer page link must be a valid URL')
        return v

    @validator('birthdate')
    def birthdate_must_be_valid(cls, v):
        if not isinstance(v, datetime):
            raise ValueError('Birthdate must be a valid datetime')
        return v

    @validator('turned_pro')
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
    id: Optional[PyObjectId] = Field(alias='_id')
    Username: str
    Email: EmailStr
    Password: str
    Teams: List[str] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    @validator('username')
    def validate_username(cls, v):
        # Add logic to check for unique username in the database
        if any(user['username'] == v for user in mock_db['users']):
            raise ValueError('Username already exists')
        return v

    @validator('email')
    def validate_email(cls, v):
        # Add logic to check for unique email in the database
        if any(user['email'] == v for user in mock_db['users']):
            raise ValueError('Email already exists')
        return v

    @validator('password')
    def validate_password(cls, v):
        # Ensure the password has at least one uppercase letter, one lowercase letter, one digit, and one special character
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$', v):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character')
        return v

class Team(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    Name: str
    OwnerId: str
    Golfers: List[str] = []
    Wins: int = Field(default=0, ge=0, description="Amount of wins a team experiences")
    Losses: int = Field(default=0, ge=0, description="Amount of losses a team experiences")
    Points: int = Field(default=0, ge=0, description="If you are a playing a league wide system, you receive points rather than wins and losses")

    class Config:
        allow_population_by_field_name = True

class League(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    Name: str
    CommissionerId: str
    Teams: List[str] = []

    class Config:
        allow_population_by_field_name = True

class Week(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    WeekNumber: int
    SeasonId: str
    Standings: List[PyObjectId]
    FreeAgentSignings: List[PyObjectId]

    @validator('WeekNumber')
    def week_number_must_be_valid(cls, v):
        if not (1 <= v <= 52):
            raise ValueError('Week number must be between 1 and 52')
        return v

class Season(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    SeasonNumber: int
    StartDate: datetime
    EndDate: datetime

    @validator('start_date', 'end_date')
    def dates_must_be_valid(cls, v, field):
        if not isinstance(v, datetime):
            raise ValueError(f'{field.name} must be a datetime')
        return v

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        start_date = values.get('start_date')
        if start_date and v <= start_date:
            raise ValueError('End date must be after start date')
        return v

class LeagueSettings(BaseModel):
    MaxGolfersPerTeam: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
    NumOfStarters: int = Field(default=2, ge=1, description="Number of defined players per team")
    MaxRosteredPlayers: int = Field(default=1, ge=0, description="Number of draft players per week")
    ScoringSystem: List[int] = Field(default_factory=lambda: [10, 8, 6, 5, 4, 3, 2, 1], description="Points awarded for placements")
    Tournaments: List[PyObjectId]
    NumOfGolferUses: Optional[int] = Field(default=None, description="Number of times a golfer can be used")
    DraftingPeriod: str = Field(default="weekly", description="Period for drafting new players")
    DraftMinutesPerPick: int
    HeadToHead: bool = Field(default=False, description="determine whether the competition is league wide or just between two users")

    @validator('num_defined_players')
    def defined_players_must_be_less_than_max(cls, v, values):
        if 'max_golfers_per_team' in values and v >= values['max_golfers_per_team']:
            raise ValueError('Number of defined players must be less than the maximum number of golfers per team')
        return v

    @validator('num_draft_players')
    def draft_players_must_fit_in_team(cls, v, values):
        if 'max_golfers_per_team' in values and 'num_defined_players' in values:
            total_players = values['num_defined_players'] + v
            if total_players > values['max_golfers_per_team']:
                raise ValueError('Number of draft players must fit within the maximum number of golfers per team')
        return v

    @validator('scoring_system')
    def scoring_system_must_be_non_negative(cls, v):
        if any(points < 0 for points in v):
            raise ValueError('Scoring system must have non-negative points')
        return v

    @validator('drafting_period')
    def drafting_period_must_be_valid(cls, v):
        if v not in ["weekly", "biweekly", "monthly"]:
            raise ValueError('Drafting period must be one of: "weekly", "biweekly", "monthly"')
        return v

    @root_validator(pre=True)
    def set_num_of_golfer_uses_default(cls, values):
        if 'num_of_golfer_uses' not in values or values['num_of_golfer_uses'] is None:
            values['num_of_golfer_uses'] = len(values.get('tournaments', []))
        return values

class DraftPick(BaseModel):
    Id: Optional[PyObjectId] = Field(alias='_id')
    TeamId: str
    GolferId: str
    RoundNumber: int
    PickNumber: int

    @validator('RoundNumber', 'PickNumber')
    def pick_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Round number and pick number must be positive')
        return v


class Draft(BaseModel):
    Id: Optional[PyObjectId] = Field(alias='_id')
    LeagueId: str
    StartDate: datetime
    EndDate: Optional[datetime] = None
    Rounds: int
    Picks: List[DraftPick]

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