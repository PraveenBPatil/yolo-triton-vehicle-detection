
from multiprocessing import Process, Queue

def worker(queue):
    message = queue.get()
    print("Worker received:", message)

if __name__ == "__main__":
    queue = Queue()

    p = Process(target=worker, args=(queue,))
    p.start()

    queue.put("Hello from the main process!")

    p.join()
    print("Communication completed!")
