# TDE - Performance em Sistemas Ciberfísicos 
Grupo 14
Fernanda Collere Milaneze, Igor Brevesteky de Paula, Leandro Tomasetto, Marcelo Bellon Ferreira Junior e Yumi Komatsu
Linguagem utilizada: Python
Instruções de compilação e execução:
Link do vídeo: 

## PARTE 1 - Jantar dos filósofos
Cinco filósofos estão sentados em uma mesa circular, alternando entre pensar e comer. Para comer, cada filósofo precisa dos dois garfos, à sua esquerda e direita. O problema é que há 5 garfos para 5 filósofos, então para alguns comerem os outros devem esperar até serem soltos os 2 garfos.
Na 1 versão, todos seguem o mesmo protocolo de pegar primeiro o garfo a esquerda e depois à direita. Então, se todos os cinco sentirem fome, cada um pegará o seu garfo da esquerda. Quando tentarem pegar o garfo da direita, todos ficarão bloqueados pra sempre, pois o garfo vizinho já estará ocupado. Isso resulta em um Deadlock, onde nenhuma thread progride.

Para o deadlock, precisam existir: exclusão mútua, manter-e-esperar, não preempção e espera circular (condições de Coffman). Na solução corrigida, usamos a Hierarquia de Recursos. Quando é verificado qual indice do garfo é menor ou maior, a Espera Circular é negada. O último filósofo (filósofo 4) inverte a ordem, tenta pegar o garfo 0 antes do 4, quebrando o ciclo de dependência na mesa, garantindo o progresso.

Pseudocódigo:
```
Definir N = 5
Definir garfo_esquerda = p
Definir garfo_direita = (p + 1) % N

Enquanto o programa rodar:
    Pensar por um tempo aleatório
    Definir estado para "com fome"
    
    Se garfo_esquerda < garfo_direita:
        primeiro_garfo = garfo_esquerda
        segundo_garfo = garfo_direita
    Senão:
        primeiro_garfo = garfo_direita
        segundo_garfo = garfo_esquerda
    
    Bloquear/Adquirir(primeiro_garfo)
    Bloquear/Adquirir(segundo_garfo)
    
    Comer por um tempo aleatório
    
    Liberar(segundo_garfo)  // Boa prática: liberação inversa
    Liberar(primeiro_garfo)
```

## PARTE 2 - Threads e semáforos
Testado com Python 3.12

Sobre o trabalho:
Criamos t = 8 threads que incrementam um mesmo contador compartilhado m = 200.000 vezes cada. O valor correto no final deveria ser t x m = 1.600.000.
O programa roda duas versões: a versão 1, sem nenhuma sincronização e a versão 2, com um semáforo binário. Cada versão é executada 4 vezes.


Resultado com 4 execuções de cada versão:
```
Valor esperado: 1600000 (8 threads, 200000 incrementos por thread)

 ----------------- Versão 1 - Sem sincronização, pode perder incrementos se ler ao mesmo tempo -------------------------
Execução 1
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 73940500 ns (73.941 ms)

Execução 2
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 74901100 ns (74.901 ms)

Execução 3
esperado: 1600000
obtido: 1400000
perdidos: 200000
tempo: 72559900 ns (72.560 ms)

Execução 4
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 72521100 ns (72.521 ms)

 --------------------- Versão 2 - Semáforo binario -------------------------------------
Execução 1
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 1140080600 ns (1140.081 ms)

Execução 2
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 1150359600 ns (1150.360 ms)

Execução 3
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 1110094800 ns (1110.095 ms)

Execução 4
esperado: 1600000
obtido: 1600000
perdidos: 0
tempo: 1102104000 ns (1102.104 ms)

```
Por que a versão sem sincronização perde incrementos?
Incrementar o contador não é uma única operação, são 3 passos separados: Primeiro, ler o valor atual do contador, depois somar 1 e então escrever o resultado de volta no contador. Porém, entre ler e escrever, outra thread pode entrar no meio, e como as 8 threads compartilham o mesmo contador e rodam ao mesmo tempo, elas podem acabar lendo o mesmo valor antigo, as duas somam 1 e então um dos incrementos é perdido.
Exemplo: O contador está em 500, uma thread lê o 500 do contador, soma +1 e então, antes de escrever, troca para outra thread. Essa outra thread também vai ler o 500 e somar  + 1, pois a primeira ainda não escreveu 501. Aconteceram 2 incrementos, mas o contador só adicionou 1, o outro incremento foi perdido. Então o contador fica em 501 em vez de 502 que seria o correto. Como isso ocorre muitas vezes ao longo da execução, o valor final fica abaixo do esperado. 
Isso é a condição de corrida, o resultado depende da ordem em que o escalonador alterna as threads.

Por que a versão com semáforo é correta?
O semáforo binário tem só 1 permissão. O método acquire() utiliza essa permissão, se outra thread já está usando essa permissão, a chamada bloqueia até ser devolvida pelo release(), isso garante a exclusão mútua (uma thread por vez pode acessar um recurso compartilhado). Então, apenas uma thread por vez executa os passos de ler, somar e escrever. Nenhuma thread consegue ler o contador enquanto outra está utilizando, então nenhum incremento é perdido e o resultado é sempre 1.600.000.
O try e finnaly garantem que a permissão seja devolvida mesmo que ocorra um erro no processo de ler, somar e compartilhar, evitando que trave o sistema.

Trade-off de throughput:
A versão sem semáforo: tem throughput mais alto. As 8 threads incrementam ao mesmo tempo, sem esperar nada. É rápida, mas o resultado está errado, mais ou menos 72ms.
A versão com semáforo: tem um throughput que é mais baixo, as threads precisam esperar a sua vez. É mais lenta mas o resultado está correto, mais ou menos 1120ms.

Visibilidade/ordenação - barreira implícitas:
Visibilidade é garantir que a escrita de uma thread fique visível para as outras. No nosso código, quando uma thread usa contador = soma_um(valor), a próxima thread que for ler valor = contador precisa enxergar esse valor novo. Então, a troca de threads entre as operações é o que causa o problema central.

Ordenação é fazer com que as operações aconteçam na ordem esperada. Compiladores podem mudar a ordem das instruções para otimizar, e no java é o happens before que impede que isso, ou os caches do processador façam uma thread ver a leitura e a escrita de outra fora de ordem. No nosso caso (python) com o CPython e o GIL, a perda de incrementos não veio da reordenação nem do cache, e sim da troca de thread entre as operações.

No CPython (interpretador), temos o GIL (global interpreter lock), que faz apenas uma thread executar código por vez, e as barreiras de memória, o semaforo.acquire() e o semaforo.release(), que fazem com que a escrita no contador esteja correta para a próxima thread que adquirir a permissão. Por isso, na versão com semáforo, a thread sempre lê o valor atualizado e o resultado da sempre 1,600,000.
Porém, o GIL protege cada passo isolado, o semáforo protege a sequência inteira como um bloco. O GIL garante atomicidade (sem ser interrompida no meio) apenas de instruções individuais (bytecodes), e não deixa atomica a sequência valor = contador e contador = soma_um(valor). Como são operações separadas, o interpretador pode trocar de thread entre elas, e é essa brecha que faz a versão sem semáforo perder incrementos.
