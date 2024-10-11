from typing import List, Optional, Tuple, Dict
from pydantic import BaseModel, Field, EmailStr, root_validator, model_validator, field_validator
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import random
import pytz

# Add this line to ensure the correct path
import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import db

import re

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

