from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import os
from flask_socketio import SocketIO

passcode = os.getenv("MONGO_PASSWORD")

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False
socketio = SocketIO(app, cors_allowed_origins="*")

api = Api(app)

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.scramble