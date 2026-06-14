import threading
import time

t = 8 # número de threads
m = 200000 # incrementos por thread
esperado = t * m
contador = 0
semaforo = threading.Semaphore(1)  # semáforo binario (1 permissão)

def soma_um(valor):
    #ler, somar, escrever
    return valor + 1

# Versão 1 - Sem sincronização, pode perder incrementos se ler ao mesmo tempo
def incrementar_sem_semaforo():
    global contador
    for c in range(m):
        valor = contador # le
        contador = soma_um(valor) # soma e escreve, += 1 nao funcionou

# Versão 2 - Semáforo binario, entra 1 por vez
def incrementar_com_semaforo():
    global contador
    for c in range(m):
        semaforo.acquire() #bloqueia
        try:
            valor = contador
            contador = soma_um(valor)
        finally: # se der erro, n trava o programa
            semaforo.release() #devolve

def executar(tarefa, mostrar):
    global contador
    contador = 0 #zerar

    threads = []
    for c in range(t): #lista de threads
        thread = threading.Thread(target=tarefa)
        threads.append(thread)

    inicio = time.perf_counter_ns()
    for th in threads:
        th.start() # dispara todas as threads
    for th in threads:
        th.join() # espera todas terminarem
    tempo = time.perf_counter_ns() - inicio
    perdidos = esperado - contador

    print(mostrar)
    print(f"esperado: {esperado}")
    print(f"obtido: {contador}")
    print(f"perdidos: {perdidos}")
    print(f"tempo: {tempo} ns ({tempo / 1000000:.3f} ms)\n")

if __name__ == "__main__":
    print(f"Valor esperado: {esperado} ({t} threads, {m} incrementos por thread)\n")
    print(" ----------------- Versão 1 - Sem sincronização, pode perder incrementos se ler ao mesmo tempo -------------------------")
    for i in range(4):
        executar(incrementar_sem_semaforo, f"Execução {i + 1}")

    print(" --------------------- Versão 2 - Semáforo binario -------------------------------------")
    for i in range(4):
        executar(incrementar_com_semaforo, f"Execução {i + 1}")