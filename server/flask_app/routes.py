from flask import request, make_response, jsonify, requests, abort
from dotenv import load_dotenv
from bson.objectid import ObjectId

from config import db, app
from models import User

from users import users_bp
from rounds import rounds_bp
from holes import holes_bp
from golfers_tournament_details import golfers_tournament_details_bp
from tournaments import tournaments_bp

# HTTP Constants 
HTTP_SUCCESS = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_CONFLICT = 409
HTTP_SERVER_ERROR = 500
HTTP_UNPROCESSABLE_ENTITY = 422

users_collection = db.users
leagues_collection = db.leagues
teams_collection = db.teams
tournaments_collection = db.tournaments
golfers_collection = db.golfers
fantasy_league_seasons_collection = db.fantasyLeagueSeasons
golfer_tournament_details_collection = db.golfertournamentdetails

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(rounds_bp, url_prefix='/rounds')
app.register_blueprint(holes_bp, url_prefix='/holes')
app.register_blueprint(golfers_tournament_details_bp, url_prefix='/golfers_tournament_details')
app.register_blueprint(tournaments_bp, url_prefix='/tournaments')

@app.route('/start_draft', methods=['POST'])
def start_draft():
    # Your logic to start the draft
    user_id = request.json.get('user_id')
    pick_duration = request.json.get('pick_duration')

    # Start the draft timer via WebSocket
    requests.post('http://localhost:5555/start_draft_timer/', json={'user_id': user_id, 'pick_duration': pick_duration})
    return jsonify({'message': 'Draft started and timer initiated'}), 200

@app.route('/end_draft', methods=['POST'])
def end_draft():
    # Your logic to end the draft
    user_id = request.json.get('user_id')

    # Stop the draft timer via WebSocket
    requests.post('http://localhost:5555/stop_draft_timer/', json={'user_id': user_id})
    return jsonify({'message': 'Draft ended and timer stopped'}), 200

@app.route('/', methods=['GET'])
def hello_world():
    return {"routes": "working!"}
    

@app.route('/tournaments', methods=['GET'])
def get_tournaments():
    tournaments = list(tournaments_collection.find())
    return jsonify([{"_id": str(tournament["_id"]), "name": tournament["name"]} for tournament in tournaments])

@app.route('/tournaments/<tournament_id>', methods=['GET'])
def get_tournament_by_id(tournament_id):
    tournament = tournaments_collection.find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        return jsonify({
            "_id": str(tournament["_id"]),
            "name": tournament["name"],
            "start_date": tournament["start_date"],
            "venue": tournament["venue"],
            "purse": tournament.get("purse")
        })
    else:
        return abort(404, description="Tournament not found")

@app.route('/get_facebook_appId', methods=["GET"])
def get_facebook_appId():
    # Authentication: You might use a more secure method here
    # For simplicity, let's assume the request comes from an allowed origin
    if request.referrer and "http://localhost:3000/" in request.referrer:
        import os

        load_dotenv()

        client_id = os.getenv("FACEBOOK_APP_ID")

        return jsonify({"facebook_app_id": client_id}), HTTP_SUCCESS
    else:
        return jsonify({"error": "Unauthorized"}), HTTP_UNAUTHORIZED

@app.route('/me', methods=['GET'])
def auth():
    if request.method == 'GET':
        pass

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        pass

@app.route('/logout', methods=['DELETE'])
def logout():
    if request.method == 'DELETE':
        pass

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        pass

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        "username": data.get("username"),
        "email": data.get("email"),
        "password": data.get("password")
    }
    result = users_collection.insert_one(user)
    return jsonify({"_id": str(result.inserted_id), "message": "User created"}), 201


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return jsonify({"_id": str(user["_id"]), "username": user["username"], "email": user["email"]})
    else:
        return abort(404, description="User not found")


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Fetch existing user document
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        # Convert to User model instance
        existing_user = User(**user)
        
        # Update only the provided fields (partial update)
        for key, value in data.items():
            setattr(existing_user, key, value)
        
        # Save the updated user
        existing_user.save()

        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted"})
    else:
        return abort(404, description="User not found")


@app.route('/users/<user_id>/teams', methods=['GET'])
def get_user_teams(user_id):
    teams = list(teams_collection.find({"owner_id": ObjectId(user_id)}))
    return jsonify([{"_id": str(team["_id"]), "team_name": team["team_name"]} for team in teams])


@app.route("/get_client_id", methods=["GET"])
def get_client_id():
    # Authentication: You might use a more secure method here
    # For simplicity, let's assume the request comes from an allowed origin
    if request.referrer and "http://localhost:3000/" in request.referrer:
        import os

        load_dotenv()

        client_id = os.getenv("CLIENT_ID")

        return jsonify({"client_id": client_id}), HTTP_SUCCESS
    else:
        return jsonify({"error": "Unauthorized"}), HTTP_UNAUTHORIZED


@app.route('/sets/<int:id>', methods=['GET', 'POST', 'DELETE'])
def modify_sets(set_id):
    if request.method == 'GET':
        # retrieve the terms by the particular set that was selected
        # _set = Set.query.filter_by(id=set_id).first()
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)

