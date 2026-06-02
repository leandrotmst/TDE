## TDE de Ciberfísico

# PARTE 1 - Jantar dos filósofos
Cinco filósofos estão sentados em uma mesa circular, alternando entre pensar e comer. Para comer, cada filósofo precisa dos dois garfos, à sua esquerda e direita, compartilhados com os vizinhos, expondo problemas clássicos de exclusão mútua, impasse e inanição em sistemas concorrentes.
Ocorre um impasse se todos pegarem, ao mesmo tempo, o garfo da esquerda e aguardarem o da direita, pois ninguém progride e todos esperam indefinidamente, caracterizando deadlock no protocolo ingênuo de “pegar primeiro um garfo, depois o outro”.
Soluções gerais exigem negar pelo menos uma das quatro condições necessárias para deadlock — exclusão mútua, manter-e-esperar, não preempção e espera circular — sendo comum eliminar a espera circular por meio de hierarquia de recursos, usar um árbitro (garçom) ou limitar a N−1 filósofos ativos.