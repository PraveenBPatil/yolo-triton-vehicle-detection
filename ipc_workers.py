
from multiprocessing import Process, Queue
import os

def worker(task_queue):
    while True:
        task = task_queue.get()

        if task is None:
            print(f"Worker {os.getpid()} stopping")
            break

        print(f"Worker {os.getpid()} processed task {task}")

if __name__ == "__main__":
    task_queue = Queue()

    # Add tasks
    for task in range(1, 6):
        task_queue.put(task)

    # Create two workers
    workers = [
        Process(target=worker, args=(task_queue,))
        for _ in range(2)
    ]

    for p in workers:
        p.start()

    # Send one stop signal per worker
    for _ in workers:
        task_queue.put(None)

    for p in workers:
        p.join()

    print("All workers stopped")
