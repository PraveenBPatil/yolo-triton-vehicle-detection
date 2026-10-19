
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["traffic_db"]
collection = db["detections"]

# Delete one matching record
result = collection.delete_one({
    "vehicle": "truck",
    "confidence": 0.88
})

if result.deleted_count == 1:
    print("Vehicle record deleted successfully!")
else:
    print("No matching record found.")

client.close()
