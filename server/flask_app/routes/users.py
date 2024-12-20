from flask import request, jsonify, session, Blueprint
import sys
import os
from bson.objectid import ObjectId
from email_validator import validate_email, EmailNotValidError
from pydantic import ValidationError
import datetime
import random
import string

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import User, Team

users_collection = db.users
teams_collection = db.teams

users_bp = Blueprint('users', __name__)

def generate_verification_code(length=6):
    """Generates a random alphanumeric verification code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def returnable_user_dict(user: User):
    associated_leagues = []
    teams_dicts = []

    if len(user.Teams) >= 1:

        # Query to find all teams in the user's teams list
        teams = db.teams.find({"_id": {"$in": user.Teams}})

        for team in teams:
            team = Team(**team) 
            
            # Convert to dictionary here and append to teams_dicts
            team_dict = team.to_dict()

            if team.Golfers and len(team.Golfers.keys()) > 0:
                team_dict["Golfers"] = team.get_all_current_golfers()

            teams_dicts.append(team_dict)

            # Fetch league details
            league = db.leagues.find_one({"_id": ObjectId(team.LeagueId)})
            associated_leagues.append({
                "id": str(league["_id"]),
                "Name": league["Name"],
                "Game": league["LeagueSettings"]["Game"]
            })

    session['user_id'] = str(user.id)
    return {
        "Username": user.Username,
        "Email": user.Email,
        "Teams": teams_dicts,
        "Leagues": associated_leagues,
        "IsVerified": user.IsVerified
    }

@users_bp.route('/me', methods=['GET'])
def auth():
    """Returns the current authenticated user if logged in"""
    user_id = session.get('user_id')
    if user_id:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        user = User(**user)
        if user and user.IsVerified:
           return jsonify(returnable_user_dict(user)), 200
    return jsonify({"error": "Unauthorized access"}), 422

@users_bp.route('/signup', methods=['POST'])
def signup():
    """Creates a new user"""
    data = request.get_json()
    try:
        new_user = User(
            Username=data.get("username"),
            Email=data.get("email"),
            Password=data.get("password"),
            Teams=[],
            IsVerified=False,  # Account is not verified yet
            VerificationExpiresAt=datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        )
    except ValidationError as e:
        formatted_errors = {}
        for error in e.errors():
            field = error['loc'][0]  # get field name
            if field == "Username":
                formatted_errors[field] = "Username's length must be between 5 and 50 characters."
            if field == "Email":
                formatted_errors[field] = ("Email is not valid. Please utilize this format: john.doe@example.com.")
            if field == "Password":
                formatted_errors[field] = "Password must be between 8 and 50 characters long, and must include at least one uppercase letter, one lowercase letter, one digit, and one special character (!@#$%^&*()-_+=)."
        return jsonify(formatted_errors), 422  # Send this to the frontend

    does_email_exist = users_collection.find_one({"Email": new_user.Email})
    does_username_exist = users_collection.find_one({"Username": new_user.Username})

    # Check for existing email or username
    if does_email_exist and not does_username_exist:
        return jsonify({"Email": "Email already exists."}), 409
    if not does_email_exist and does_username_exist:
        return jsonify({"Username": "Username already exists."}), 409
    elif does_username_exist and does_email_exist:
        return jsonify({"Username": "Username already exists.", "Email": "Email already exists."}), 409
    
    # Hash the user's password
    new_user.Password = new_user.hash_password(new_user.Password)

    new_user.save()

    new_user.send_verification_email()

    return jsonify({"message": "User created. Check your email for the verification code."}), 201

@users_bp.route('/send_new_verify_email_code', methods=['POST'])
def request_new_code():
    data = request.get_json()
    email = data.get("email")
    
    user = users_collection.find_one({ "Email": email })

    if not user:
        return jsonify({"error": "Email not found."}), 404

    user = User(**user)

    user.send_verification_email()

    return jsonify({"message": "New verification code sent to your email."}), 200

@users_bp.route('/verify_email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get("email")
    code = data.get("code")

    # Find the user and check the code
    user = users_collection.find_one({"Email": email})
    if not user:
        return jsonify({"error": "User not found."}), 404

    if user['VerificationCode'] != code:
        return jsonify({"error": "Invalid verification code."}), 400

    # Check if the code is expired
    if user['VerificationExpiresAt'] < datetime.datetime.utcnow():
        return jsonify({"error": "Verification code expired."}), 400

    # Update the user's verification status
    users_collection.update_one({"Email": email}, {"$set": {"IsVerified": True}})

    return jsonify({
        "message": "Email successfully verified.",
    }), 200        

@users_bp.route('/login', methods=['POST'])
def login():
    """Logs in a user"""
    data = request.get_json()
    username_or_email = data.get("usernameOrEmail")
    user_data = None

    try:
        emailinfo = validate_email(username_or_email, check_deliverability=False)
        email = emailinfo.normalized
        user_data = users_collection.find_one({
        "Email": email
        })
    except EmailNotValidError:
        user_data = users_collection.find_one({
        "Username": username_or_email
        })

    if user_data:
        user = User(**user_data)
        if user.check_password(data.get("password")):
            if not user.IsVerified:
                user.send_verification_email()
            session['user_id'] = str(user.id)
            return jsonify(returnable_user_dict(user)), 200
        else:
            return jsonify({
                "error": "Password is incorrect"
            }), 422

    return jsonify({"error": "Email, username, or password is incorrect. Please try again."}), 401

@users_bp.route('/logout', methods=['DELETE'])
def logout():
    """Logs out a user"""
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@users_bp.route('/update_user', methods=['PUT'])
def update_user():
    """Updates an existing user"""
    data = request.get_json()
    user_id = session["user_id"]
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if user_data and str(user_data["_id"]) == session["user_id"]:
        user = User(**user_data)

        # Update user's fields
        if 'Username' in data:
            user.Username = data['Username']
        if 'Email' in data:
            user.Email = data['Email']

        # Password update: check if new password is the same as the current password
        if 'Password' in data:
            new_password = data['Password']
            if user.Password.check_password(new_password):
                return jsonify({"error": "New password cannot be the same as the current password"}), 400
            else:
                # Hash the new password and update
                user.Password = user.hash_password(new_password)

        user.save()
        return jsonify({
                "user": {
                    "Username": user.Username,
                    "Email": user.Email,
                    "IsVerified": user.IsVerified
                }
        }), 200
    return jsonify({"error": "You are unauthorized to change this document."}), 401

@users_bp.route('/reset_password', methods=['PUT'])
def reset_password():
    """Updates an existing user"""
    data = request.get_json()
    user_data = users_collection.find_one({"Email": data["email"]})

    if user_data:
        try: 
            user = User(**user_data)

            user.Password = user.hash_password(data['newPassword'])

            user.save()
            return jsonify({"message": "User password updated successfully"}), 200
        except ValidationError as e:
            return jsonify({
                "error": "Password must be between 8 and 50 characters long, and must include at least one uppercase letter, one lowercase letter, one digit, and one special character (!@#$%^&*()-_+=)."
            }), 422

    return jsonify({"error": "User not found"}), 404

@users_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    """Deletes a user by ID"""
    user_id = session["user_id"]
    result = users_collection.delete_one({"_id": ObjectId(user_id)})

    if not user_id:
        return jsonify({"message": "You are unauthorized to delete this user."}), 401

    if result.deleted_count > 0:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/<user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    """Fetches all teams for a given user"""
    teams = list(teams_collection.find({"owner_id": ObjectId(user_id)}))
    return jsonify([{"_id": str(team["_id"]), "TeamName": team["TeamName"]} for team in teams]), 200