
from multiprocessing import Process, Queue
from pymongo import MongoClient


def database_worker(queue):
    # This process connects to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    collection = client["traffic_db"]["detections"]

    while True:
        detection = queue.get()

        # Stop when the special signal arrives
        if detection is None:
            break

        collection.insert_one(detection)
        print("Saved to MongoDB:", detection["vehicle"])

    client.close()


if __name__ == "__main__":
    queue = Queue()

    # Start the database process
    worker = Process(target=database_worker, args=(queue,))
    worker.start()

    # Simulated detection record for this first integration test
    detection = {
        "car_id": 100,
        "vehicle": "car",
        "model": "yolo_trt",
        "confidence": 0.95,
        "bbox": [100, 50, 200, 150]
    }

    # Send the record to the database process
    queue.put(detection)

    # Tell the worker to stop after processing the record
    queue.put(None)

    worker.join()
    queue.close()

    print("Main process finished.")
