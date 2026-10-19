
from pymongo import MongoClient

# Connect Python to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select a database
db = client["traffic_db"]

# Select a collection
collection = db["detections"]

# Create one car detection record
car = {
    "car_id": 1,
    "vehicle": "car",
    "confidence": 0.92
}

# Save the record
result = collection.insert_one(car)

print("Record saved successfully!")
print("Record ID:", result.inserted_id)

client.close()
