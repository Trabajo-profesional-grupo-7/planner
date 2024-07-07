import os

from pymongo.mongo_client import MongoClient

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

uri = f"mongodb+srv://{username}:{password}@planner.pjzb60a.mongodb.net/?retryWrites=true&w=majority&ssl=true&appName=planner"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.planner_db

plans_collection = db["planner_collection"]
