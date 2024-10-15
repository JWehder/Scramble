from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import os
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_mailman import Mail
import os

# Load environment variables from .env file
load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False
socketio = SocketIO(app, cors_allowed_origins="*")

api = Api(app)

mail = Mail()

app.config["MAIL_SERVER"] = "smtp.zohomail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail.init_app(app)

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client.scramble