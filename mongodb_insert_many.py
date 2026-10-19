
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database and collection
db = client["traffic_db"]
collection = db["detections"]

# Sample vehicle detection results
vehicles = [
    {"vehicle": "car", "confidence": 0.92},
    {"vehicle": "truck", "confidence": 0.88},
    {"vehicle": "bus", "confidence": 0.95}
]

# Save all three records
result = collection.insert_many(vehicles)

print("Vehicles saved successfully!")
print("Number of records saved:", len(result.inserted_ids))

client.close()
