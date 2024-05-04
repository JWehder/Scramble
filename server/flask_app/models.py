from typing import List, Optional
from pydantic import BaseModel, Field


class Hole(BaseModel):
    _id: str
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


class Round(BaseModel):
    _id: str
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


class GolferTournamentDetails(BaseModel):
    _id: str
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
    Rounds: List[Round]
    OWGR: str


class Tournament(BaseModel):
    _id: str
    EndDate: str
    StartDate: str
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
    Golfers: List[GolferTournamentDetails]

class User(BaseModel):
    id: str
    username: str
    email: str
    password: str
    teams: List[str] = []

    class Config:
        allow_population_by_field_name = True

class Team(BaseModel):
    id: str 
    name: str
    owner_id: str
    golfers: List[str] = []

    class Config:
        allow_population_by_field_name = True

class League(BaseModel):
    id: str
    name: str
    commissioner_id: str
    teams: List[str] = []

    class Config:
        allow_population_by_field_name = True