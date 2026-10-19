
from multiprocessing import Process, Pipe

def worker(connection):
    number = connection.recv()
    print("Worker received:", number)

    result = number * number
    connection.send(result)

    connection.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=worker, args=(child_conn,))
    p.start()

    child_conn.close()

    parent_conn.send(6)

    answer = parent_conn.recv()
    print("Result from worker:", answer)

    parent_conn.close()
    p.join()
