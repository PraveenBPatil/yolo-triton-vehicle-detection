
from multiprocessing import Process, Queue

def worker(result_queue):
    try:
        number = 10
        result = number / 0

        result_queue.put(("success", result))

    except Exception as e:
        result_queue.put(("error", str(e)))

if __name__ == "__main__":
    result_queue = Queue()

    p = Process(target=worker, args=(result_queue,))
    p.start()

    status, message = result_queue.get()

    p.join()

    print("Status:", status)
    print("Message:", message)
