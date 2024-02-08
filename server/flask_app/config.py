from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False

api = Api(app)