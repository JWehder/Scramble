from flask import request, jsonify, abort, session
from . import users_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import User

users_collection = db.users
teams_collection = db.teams

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
            })
    return abort(401, description="Unauthorized")

@users_bp.route('/signup', methods=['POST'])
def signup():
    """Creates a new user"""
    data = request.get_json()
    new_user = User(
        Username=data.get("Username"),
        Email=data.get("Email"),
        Password=data.get("Password")  # Raw password, will be hashed below
    )

    # Hash the user's password using the model's method
    new_user.password = new_user.hash_password(new_user.password)

    # Check for existing email or username
    if users_collection.find_one({"Email": new_user.email}):
        return jsonify({"error": "Email already exists"}), 409
    if users_collection.find_one({"Username": new_user.username}):
        return jsonify({"error": "Username already exists"}), 409

    # Save the user using the model's `save` method
    user_id = new_user.save()
    return jsonify({"_id": str(user_id), "message": "User created successfully"}), 201

@users_bp.route('/login', methods=['POST'])
def login():
    """Logs in a user"""
    data = request.get_json()
    user_data = users_collection.find_one({"Email": data.get("Email")})

    if user_data:
        user = User(**user_data)
        # Check if the password matches using the model's method
        if user.check_password(data.get("Password")):
            session['user_id'] = str(user.id)  # Set the user_id in the session
            return jsonify({"message": "Login successful"})
    
    return abort(401, description="Invalid credentials")

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
        })
    return abort(404, description="User not found")

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
            # Hash the new password before saving
            user.Password = user.hash_password(data['Password'])
        
        # Save the updated user using the model's `save` method
        user.save()
        return jsonify({"message": "User updated successfully"}), 200
    
    return abort(404, description="User not found")

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user by ID"""
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted"}), 200
    return abort(404, description="User not found")

@users_bp.route('/users/<user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    """Fetches all teams for a given user"""
    teams = list(teams_collection.find({"owner_id": ObjectId(user_id)}))
    return jsonify([{"_id": str(team["_id"]), "TeamName": team["TeamName"]} for team in teams]), 200