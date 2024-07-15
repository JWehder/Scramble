from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

passcode = os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://jakewehder:{passcode}@cluster0.gbnbssg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB Connection
client = MongoClient(uri)
db = client.scramble

# Specify the regular expression pattern
pattern = "^\w+\s\w+$"

# Find documents where the last name matches the pattern
results = db.golfers.find({"LastName": {"$regex": pattern}})

# Iterate over the results
for result in results:
    print(result)

# Find documents where the last name contains "Mc"
results = db.golfers.find({"LastName": {"$regex": "Mc"}})

for result in results:
    print(result)

client.close()