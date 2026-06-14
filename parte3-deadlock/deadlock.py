import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def thread_1():
    print("Thread 1: tentando adquirir LOCK_A")
    LOCK_A.acquire()
    print("Thread 1: adquiriu LOCK_A")

    time.sleep(0.05)

    print("Thread 1: tentando adquirir LOCK_B")
    LOCK_B.acquire()  
    print("Thread 1: adquiriu LOCK_B")

    LOCK_B.release()
    LOCK_A.release()
    print("Thread 1 concluiu")


def thread_2():
    print("Thread 2: tentando adquirir LOCK_B")
    LOCK_B.acquire()
    print("Thread 2: adquiriu LOCK_B")

    time.sleep(0.05)

    print("Thread 2: tentando adquirir LOCK_A")
    LOCK_A.acquire()  
    print("Thread 2: adquiriu LOCK_A")

    LOCK_A.release()
    LOCK_B.release()
    print("Thread 2 concluiu")


if __name__ == "__main__":
    
    t1 = threading.Thread(target=thread_1)
    t2 = threading.Thread(target=thread_2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Fim do programa")