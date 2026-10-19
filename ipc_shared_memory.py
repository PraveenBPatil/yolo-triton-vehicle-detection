
from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory

def worker(shm_name):
    shm = SharedMemory(name=shm_name)

    data = bytes(shm.buf[:5])
    print("Worker received:", data.decode())

    shm.close()

if __name__ == "__main__":
    shm = SharedMemory(create=True, size=5)

    try:
        shm.buf[:5] = b"HELLO"

        p = Process(target=worker, args=(shm.name,))
        p.start()
        p.join()

    finally:
        shm.close()
        shm.unlink()
