
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["traffic_db"]
collection = db["detections"]

# Find cars with confidence greater than 0.80
records = collection.find({
    "vehicle": "car",
    "confidence": {"$gt": 0.80}
})

for record in records:
    print(record)

client.close()
