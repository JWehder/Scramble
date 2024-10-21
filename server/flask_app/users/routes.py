from flask import request, jsonify, abort, session
from . import users_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId
from .model import User
from email_validator import validate_email, EmailNotValidError
from pydantic import ValidationError
import datetime
import random
import string

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

users_collection = db.users
teams_collection = db.teams

def generate_verification_code(length=6):
    """Generates a random alphanumeric verification code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

@users_bp.route('/me', methods=['GET'])
def auth():
    """Returns the current authenticated user if logged in"""
    user_id = session.get('user_id')
    if user_id:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return jsonify({
                "_id": str(user["_id"]), 
                "Username": user["Username"], 
                "Email": user["Email"],
                "Teams": user.get("Teams", [])
            }), 200
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
            IsVerified=False,  # Account is not verified yet
            VerificationExpiresAt=datetime.datetime.utcnow() + datetime.timedelta(hours=24)
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

@users_bp.route('/request_new_code', methods=['POST'])
def request_new_code():
    data = request.get_json()
    email = data.get("email")
    
    user = users_collection.find_one({ "Email": email })
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

    return jsonify({"message": "Email successfully verified."}), 200                      

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
        "IsVerified": True,
        "VerificationExpiresAt": {"$gt": datetime.datetime.utcnow()},
        "Email": email
        })
    except EmailNotValidError:
        user_data = users_collection.find_one({
        "IsVerified": True,
        "VerificationExpiresAt": {"$gt": datetime.datetime.utcnow()},
        "Username": username_or_email
        })

    if user_data and user_data['IsVerified']:
        user = User(**user_data)
        if user.check_password(data.get("password")):
            session['user_id'] = str(user.id)
            return jsonify({"message": "Login successful"}), 200
    else:
        user = User(**user_data)
        user.send_verification_email()
        return jsonify({"message": "Login successful when email is verified."}), 200


    return jsonify({"error": "Email, username, or password is incorrect. Please try again."}), 401

@users_bp.route('/logout', methods=['DELETE'])
def logout():
    """Logs out a user"""
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Fetches a user by ID"""
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        user = User(**user_data)
        return jsonify({
            "_id": str(user.id),
            "Username": user.Username,
            "Email": user.Email,
            "Teams": user.Teams
        }), 200

    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user"""
    data = request.get_json()
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if user_data:
        user = User(**user_data)

        # Update user's fields
        if 'Username' in data:
            user.Username = data['Username']
        if 'Email' in data:
            user.Email = data['Email']
        if 'Password' in data:
            user.Password = user.hash_password(data['Password'])

        user.save()
        return jsonify({"message": "User updated successfully"}), 200

    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user by ID"""
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    """Fetches all teams for a given user"""
    teams = list(teams_collection.find({"owner_id": ObjectId(user_id)}))
    return jsonify([{"_id": str(team["_id"]), "TeamName": team["TeamName"]} for team in teams]), 200