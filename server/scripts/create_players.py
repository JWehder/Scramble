from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client["scramble"]
collection = db["golfers"]

print(collection)

client.close()
