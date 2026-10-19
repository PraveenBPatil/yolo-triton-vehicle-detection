
from multiprocessing import Process, Queue

def worker(task_queue, result_queue):
    number = task_queue.get()

    result = number * number

    result_queue.put(result)

if __name__ == "__main__":
    task_queue = Queue()
    result_queue = Queue()

    p = Process(
        target=worker,
        args=(task_queue, result_queue)
    )

    p.start()

    task_queue.put(5)

    answer = result_queue.get()

    print("Worker returned:", answer)

    p.join()
