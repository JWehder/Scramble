from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from bson import ObjectId

# Add this line to ensure the correct path
import sys
import os

# Adjust the paths for MacOS to get the server directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import PyObjectId 
from config import db

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

    def save(self) -> Optional[ObjectId]:
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