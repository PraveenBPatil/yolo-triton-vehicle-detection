
from threading import Thread
import time

def worker():
    print("Worker started")
    time.sleep(2)
    print("Worker finished")

if __name__ == "__main__":
    t = Thread(target=worker)

    t.start()

    print("Main continues working")

    t.join()

    print("Main finished")
