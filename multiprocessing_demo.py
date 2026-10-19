
from multiprocessing import Process
import time

def worker():
    print("worker: started working")
    time.sleep(3)
    print("worker: finished working")

if __name__ == "__main__":
    p = Process(target=worker)

    print("main: starting worker")
    p.start()

    print("main: waiting for worker")
    p.join()

    print("main:finished")
