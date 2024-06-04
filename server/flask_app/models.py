from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from bson import ObjectId

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
    id: Optional[PyObjectId] = Field(alias='_id')
    strokes: int
    par: bool
    net_score: int
    hole_number: int
    birdie: bool
    bogey: bool
    eagle: bool
    albatross: bool
    double_bogey: bool
    worse_than_double_bogey: bool
    golfer_tournament_details_id: str
    round_id: str

    @validator('strokes')
    def strokes_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Strokes must be at least 1')
        return v

    @validator('hole_number')
    def hole_number_must_be_valid(cls, v):
        if not (1 <= v <= 18):
            raise ValueError('Hole number must be between 1 and 18')
        return v

class Round(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    golfer_tournament_details_id: str
    round: str
    birdies: int
    eagles: int
    pars: int
    albatross: int
    bogeys: int
    double_bogeys: int
    worse_than_double_bogeys: int
    score: int
    holes: List[Hole]

    @validator('score')
    def score_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('Score must be positive')
        return v

class GolferTournamentDetails(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    golfer_id: str
    position: str
    name: str
    score: str
    r1: str
    r2: str
    r3: str
    r4: str
    total_strokes: str
    earnings: str
    fedex_pts: str
    tournament_id: str
    rounds: List[Round]
    owgr: str

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
    username: str
    email: EmailStr
    password: str
    teams: List[str] = []

    class Config:
        allow_population_by_field_name = True

class Team(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    owner_id: str
    golfers: List[str] = []

    class Config:
        allow_population_by_field_name = True

class League(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    commissioner_id: str
    teams: List[str] = []

    class Config:
        allow_population_by_field_name = True

class Week(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    week_number: int
    season_id: str

    @validator('week_number')
    def week_number_must_be_valid(cls, v):
        if not (1 <= v <= 52):
            raise ValueError('Week number must be between 1 and 52')
        return v

class Season(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    season_number: int
    start_date: datetime
    end_date: datetime

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
    max_golfers_per_team: int = Field(default=3, ge=1, description="Maximum number of golfers per team")
    num_defined_players: int = Field(default=2, ge=1, description="Number of defined players per team")
    num_draft_players: int = Field(default=1, ge=0, description="Number of draft players per week")
    scoring_system: List[int] = Field(default_factory=lambda: [10, 8, 6, 5, 4, 3, 2, 1], description="Points awarded for placements")
    num_tournaments: int = Field(ge=1, description="Number of tournaments in the league season")
    allow_multiple_uses: bool = Field(default=False, description="Whether a golfer can be used multiple times")
    is_keeper_league: bool = Field(default=False, description="Whether the league is a keeper league")
    drafting_period: str = Field(default="weekly", description="Period for drafting new players")
    
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