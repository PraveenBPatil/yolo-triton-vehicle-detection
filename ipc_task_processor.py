
from multiprocessing import Process, Queue

def worker(task_queue, result_queue):
    while True:
        number = task_queue.get()

        # Stop when we receive None
        if number is None:
            break

        result = number * number

        result_queue.put((number, result))

if __name__ == "__main__":
    task_queue = Queue()
    result_queue = Queue()

    # Create a worker process
    p = Process(
        target=worker,
        args=(task_queue, result_queue)
    )
    p.start()

    # Send tasks to the worker
    numbers = [2, 3, 4, 5]

    for number in numbers:
        task_queue.put(number)

    # Tell the worker to stop after its tasks
    task_queue.put(None)

    # Receive results
    for _ in numbers:
        number, result = result_queue.get()
        print(f"Square of {number} = {result}")

    p.join()

    task_queue.close()
    result_queue.close()

    print("All tasks completed!")
