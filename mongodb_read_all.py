
from pymongo import MongoClient

# 1. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 2. Select database
db = client["traffic_db"]

# 3. Select collection
collection = db["detections"]

# 4. Read all records
records = collection.find()

# 5. Display each record
for record in records:
    print(record)

# 6. Close connection
client.close()
