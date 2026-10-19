
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["traffic_db"]
collection = db["detections"]

# Update one car record
result = collection.update_one(
    {"vehicle": "car", "confidence": 0.92},
    {"$set": {"confidence": 0.97}}
)

if result.matched_count > 0:
    print("Vehicle record found.")
    print("Records updated:", result.modified_count)
else:
    print("No matching record found.")

client.close()
