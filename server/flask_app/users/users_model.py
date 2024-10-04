from pydantic import BaseModel, Field, EmailStr, root_validator, model_validator, field_validator
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt
import os
import sys

# Adjust the paths for MacOS to get the server directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import PyObjectId 
from config import db

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    username: str
    email: EmailStr
    password: str
    teams: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    def save(self):
        """Insert or update a user"""
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = self.updated_at

        user_data = self.dict(by_alias=True, exclude_unset=True)
        if '_id' in user_data and user_data['_id']:
            # Update existing user
            result = db.users.update_one({'_id': user_data['_id']}, {'$set': user_data})
            if result.matched_count == 0:
                raise ValueError(f"User not found with _id: {user_data['_id']}")
        else:
            # Insert new user
            result = db.users.insert_one(user_data)
            self.id = result.inserted_id
        return self.id

    def hash_password(self, password: str) -> str:
        """Hash a plain text password"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check a plain text password against the stored hashed password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @field_validator('username')
    def validate_username_length(cls, v):
        """Ensure username is at least 5 characters long"""
        if len(v) < 5:
            raise ValueError('Username must be at least 5 characters long.')
        return v

    @field_validator('password')
    def validate_password_strength(cls, v):
        """Ensure password meets complexity requirements"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit.')
        if not any(char in "!@#$%^&*()-_+=" for char in v):
            raise ValueError('Password must contain at least one special character.')
        return v