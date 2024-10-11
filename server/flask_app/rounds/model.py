from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from bson import ObjectId

# Add this line to ensure the correct path
import sys
import os

# Adjust the paths for MacOS to get the server directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import PyObjectId 
from config import db

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