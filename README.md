# DS using Consumer-Producer Pattern

O código implementa o padrão produtor-consumidor, onde o produtor é a classe SensorMonitor e o consumidor é a classe MessageBroker. 
O objetivo é simular a leitura de sensores e publicar os valores lidos em uma fila de mensagens para que o consumidor possa consumi-las.
O produtor, SensorMonitor, é responsável por ler os valores dos sensores em um loop e publicá-los na fila de mensagens 
através do método publish do objeto MessageBroker. A cada leitura do sensor, o produtor cria uma mensagem com o 
nome do sensor e o valor lido, e publica essa mensagem na fila.
O consumidor, MessageBroker, é responsável por consumir as mensagens publicadas na fila de mensagens através do método consume. 
Esse método é executado em um loop infinito, onde a cada iteração ele tenta obter uma mensagem da fila. 
Se uma mensagem estiver disponível, ele a consome e a exibe na saída padrão.
No código, o produtor é iniciado primeiro, seguido pelo consumidor. 

Para persistencia à falhas, o código implementa o padrão replicação ativa.
O código cria 3 réplicas do sistema, cada uma com um produtor e um consumidor.
Cada réplica é iniciada em uma thread separada.
Para simular a falha de uma das réplicas, o código remove uma das réplicas da lista de réplicas ativas
E para o produtor e o consumidor da réplica.
Observa-se que as outras réplicas continuam funcionando normalmente.
Após 5 segundos depois da falha, paramos o produtor e o consumidor de cada réplica
Para parar a simulação.


Executar o código:
`python3 pc.py`
