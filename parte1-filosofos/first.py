import threading
import time
import random

N = 5

garfos = []
for _ in range(N):
    garfos.append(threading.Lock())

def interacoes(id_filosofo):
    while True:
        garfo_esquerda = id_filosofo
        garfo_direita = (id_filosofo + 1) % N
        print(f"Filósofo {id_filosofo} com fome...")
        garfos[garfo_esquerda].acquire()
        time.sleep(0.1)
        garfos[garfo_direita].acquire()
        print(f"Filósofo {id_filosofo} comendo...")
        time.sleep(random.uniform(0.5, 1.5))
        garfos[garfo_direita].release()
        garfos[garfo_esquerda].release()
        print(f"Filósofo {id_filosofo} pensando...")
        time.sleep(random.uniform(0.5, 1.5))

threads_filosofos = []
for i in range(N):
    thread = threading.Thread(target=interacoes, args=[i])
    threads_filosofos.append(thread)
    thread.start()
