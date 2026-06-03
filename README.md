## TDE de Ciberfísico

# PARTE 1 - Jantar dos filósofos
Cinco filósofos estão sentados em uma mesa circular, alternando entre pensar e comer. Para comer, cada filósofo precisa dos dois garfos, à sua esquerda e direita. O problema é que há 5 garfos para 5 filósofos, então para alguns comerem os outros devem esperar até serem soltos os 2 garfos.
Na 1 versão, todos seguem o mesmo protocolo de pegar primeiro o garfo a esquerda e depois à direita. Então, se todos os cinco sentirem fome, cada um pegará o seu garfo da esquerda. Quando tentarem pegar o garfo da direita, todos ficarão bloqueados pra sempre, pois o garfo vizinho já estará ocupado. Isso resulta em um Deadlock, onde nenhuma thread progride.

Para o deadlock, precisam existir: exclusão mútua, manter-e-esperar, não preempção e espera circular (condições de Coffman). Na solução corrigida, usamos a Hierarquia de Recursos. Quando é verificado qual indice do garfo é menor ou maior, a Espera Circular é negada. O último filósofo (filósofo 4) inverte a ordem, tenta pegar o garfo 0 antes do 4, quebrando o ciclo de dependência na mesa, garantindo o progresso.

Pseudocódigo:
```
python
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
