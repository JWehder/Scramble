from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import requests
import sys

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False

api = Api(app)

uri = "mongodb+srv://pauljhamlin:d121BRmy5o6W0VQu@cluster0.1pr8iip.mongodb.net"
client = MongoClient(uri)

import requests

url = "https://api.sportradar.com/golf/trial/pga/v3/en/2024/players/statistics.json?api_key=Yi0OEWrTnt8iz5tv75C7J1KH5gjJKATk6MjyMkl8"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

data = response.json()

# Approximate size in bytes
data_size_bytes = sys.getsizeof(data) 

# Convert to more readable units if needed 
data_size_mb = data_size_bytes / (1024 * 1024)  
print("Data size (approximately): {:.2f} MB".format(data_size_mb))

content_length = int(response.headers.get('Content-Length', 0))

print(content_length)

print(len(data["players"]))

