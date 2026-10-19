from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database and collection
db = client["traffic_db"]
collection = db["detections"]

# Read one record
car = collection.find_one()

print("Car record:")
print(car)

# Close connection
client.close()