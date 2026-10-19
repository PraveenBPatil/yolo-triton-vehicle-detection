
from pymongo import MongoClient
from datetime import datetime, timezone

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database and collection
db = client["traffic_db"]
collection = db["detections"]

# Example detection result
detection = {
    "vehicle": "car",
    "confidence": 0.92,
    "model": "yolo_trt",
    "timestamp": datetime.now(timezone.utc)
}

# Save the detection
result = collection.insert_one(detection)

print("Detection saved successfully!")
print("MongoDB document ID:", result.inserted_id)

client.close()
