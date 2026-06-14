import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()


def tarefa(identificador):
    print(f"Thread {identificador}: tentando adquirir LOCK_A")
    LOCK_A.acquire()
    print(f"Thread {identificador}: adquiriu LOCK_A")

    time.sleep(0.05)

    print(f"Thread {identificador}: tentando adquirir LOCK_B")
    LOCK_B.acquire()
    print(f"Thread {identificador}: adquiriu LOCK_B")

    LOCK_B.release()
    LOCK_A.release()
    print(f"Thread {identificador} concluiu")


if __name__ == "__main__":
    t1 = threading.Thread(target=tarefa, args=(1,))
    t2 = threading.Thread(target=tarefa, args=(2,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Fim do programa (sem deadlock)")