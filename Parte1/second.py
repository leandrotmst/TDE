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

        if garfo_esquerda < garfo_direita:
            primeiro_garfo = garfo_esquerda
            segundo_garfo = garfo_direita
        else:
            primeiro_garfo = garfo_direita
            segundo_garfo = garfo_esquerda

        print(f"Filósofo {id_filosofo} pensando...")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"Filósofo {id_filosofo} com fome...")
        garfos[primeiro_garfo].acquire()
        time.sleep(0.1)
        garfos[segundo_garfo].acquire()
        print(f"Filósofo {id_filosofo} comendo...")
        time.sleep(random.uniform(0.5, 1.5))
        garfos[segundo_garfo].release()
        garfos[primeiro_garfo].release()


threads_filosofos = []
for i in range(N):
    thread = threading.Thread(target=interacoes, args=[i])
    threads_filosofos.append(thread)
    thread.start()
