from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, Dict
from datetime import datetime
from bson import ObjectId

# Add this line to ensure the correct path
import sys
import os

# Adjust the paths for MacOS to get the server directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import PyObjectId 
from config import db

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

    # This is simply for free agent signings, uses will be tallied later when
    # the tournament starts.
    def sign_free_agent(self, free_agent_id: str, period_id: PyObjectId):
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

    # Either add the golfer to the team or add another use for an existing 
    # golfer.
    # Also, bench golfers if explicitly told to.
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
            self.Golfers[golfer_id_str]['CurrentlyOnTeam'] = True
            if bench:
                self.set_golfer_as_bench(golfer_id)
            elif not bench:
                self.set_golfer_as_starter(golfer_id)
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
