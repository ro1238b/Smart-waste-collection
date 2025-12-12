from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["smart_waste_db"]

# Collections
bins_collection = db["bins"]
recordings_collection = db["recordings"]


def fetch_data():
    """Fetch latest reading per bin from recordings collection."""
    pipeline = [
        {"$sort": {"timestamp": -1}},  # latest first
        {"$group": {"_id": "$bin_id", "doc": {"$first": "$$ROOT"}}}
    ]
    latest_docs = [item["doc"] for item in recordings_collection.aggregate(pipeline)]

    # Convert _id and timestamp
    for doc in latest_docs:
        doc["_id"] = str(doc["_id"])
        if isinstance(doc["timestamp"], str):
            doc["timestamp"] = datetime.fromisoformat(doc["timestamp"])
    return latest_docs


def fetch_bin(bin_id):
    """Fetch bin details from bins collection."""
    return bins_collection.find_one({"bin_id": bin_id})

