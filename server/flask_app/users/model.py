from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt
import os
import sys
from email_validator import validate_email, EmailNotValidError

# Adjust the paths for MacOS to get the server directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import PyObjectId 
from config import db

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    Username: str
    Email: EmailStr
    Password: str
    Teams: List[str] = []
    VerificationCode: Optional[str] = 0
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
        print(password, self.Password)
        """Check a plain text password against the stored hashed password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.Password.encode('utf-8'))

    @field_validator('Username')
    def validate_username_length(cls, v):
        """Ensure username is at least 5 characters long"""
        if len(v) < 5 or len(v) > 50:
            raise ValueError('Username length must be between 5 and 50 characters.')
        return v

    @field_validator('Email')
    def validate_email_and_deliverability(cls, v):
        """Ensure that the email is valid and deliverable"""
        try:
            # Check that the email address is valid. Turn on check_deliverability
            emailinfo = validate_email(v, check_deliverability=True)

            # After this point, use only the normalized form of the email address,
            # especially before going to a database query.
            email = emailinfo.normalized
            return email

        except EmailNotValidError as e:

            # The exception message is human-readable explanation of why it's
            # not a valid (or deliverable) email address.
            return str(e)

    @field_validator('Password')
    def validate_password_strength(cls, v):
        """Ensure password meets complexity requirements"""
        if len(v) < 8 or len(v) > 50:
            raise ValueError('Password must be between 8 and 50 characters.')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit.')
        if not any(char in "!@#$%^&*()-_+=" for char in v):
            raise ValueError('Password must contain at least one special character.')
        return v