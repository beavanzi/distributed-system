# Academica: Beatriz Avanzi Ecli        RA: 108612

# O código implementa o padrão produtor-consumidor, onde o produtor é a classe SensorMonitor e o consumidor é a classe MessageBroker. 
# O objetivo é simular a leitura de sensores e publicar os valores lidos em uma fila de mensagens para que o consumidor possa consumi-las.
# O produtor, SensorMonitor, é responsável por ler os valores dos sensores em um loop e publicá-los na fila de mensagens 
# através do método publish do objeto MessageBroker. A cada leitura do sensor, o produtor cria uma mensagem com o 
# nome do sensor e o valor lido, e publica essa mensagem na fila.
# O consumidor, MessageBroker, é responsável por consumir as mensagens publicadas na fila de mensagens através do método consume. 
# Esse método é executado em um loop infinito, onde a cada iteração ele tenta obter uma mensagem da fila. 
# Se uma mensagem estiver disponível, ele a consome e a exibe na saída padrão.
# No código, o produtor é iniciado primeiro, seguido pelo consumidor. 

# Para persistencia à falhas, o código implementa o padrão replicação ativa.
# O código cria 3 réplicas do sistema, cada uma com um produtor e um consumidor.
# Cada réplica é iniciada em uma thread separada.
# Para simular a falha de uma das réplicas, o código remove uma das réplicas da lista de réplicas ativas
# E para o produtor e o consumidor da réplica.
# Observa-se que as outras réplicas continuam funcionando normalmente.
# Após 5 segundos depois da falha, paramos o produtor e o consumidor de cada réplica
# Para parar a simulação.


import random
import time
import threading
import queue

class Sensor:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def read(self):
        # Simula a leitura do valor do sensor
        self.value = random.randint(0, 100)
        return self.value

class MessageBroker:
    def __init__(self):
        self.queue = queue.Queue()
        self.running = True

    def publish(self, message):
        self.queue.put(message)

    def consume(self):
        while self.running:
            try:
                message = self.queue.get(timeout=1)
                print(f"Consumed message: {message}")
            except queue.Empty:
                pass

    def start(self):
        self.running = True
        t = threading.Thread(target=self.consume)
        t.start()

    def stop(self):
        self.running = False


class SensorMonitor:
    def __init__(self, sensors, message_broker):
        self.sensors = sensors
        self.message_broker = message_broker
        self.running = False

    def start(self):
        self.running = True
        t = threading.Thread(target=self._monitor_loop)
        t.start()

    def stop(self):
        self.running = False

    def _monitor_loop(self):
        while self.running:
            # Lê os valores dos sensores
            for sensor in self.sensors:
                value = sensor.read()
                # Publica os valores lidos na fila de mensagens
                self.message_broker.publish(f"{sensor.name}: {value}")
            time.sleep(1)


if __name__ == "__main__":
        # Cria as replicas do sistema
    replicas = []
    for i in range(3):
        # Cria os sensores
        sensors = [Sensor(f"Sensor-{j}") for j in range(5)]
        # Cria o message broker
        message_broker = MessageBroker()
        # Cria o monitor de sensores
        monitor = SensorMonitor(sensors, message_broker)
        replicas.append({'monitor': monitor, 'consumer': message_broker})

    # Inicia os monitores de sensores
    for replica in replicas:
        replica['monitor'].start()
        replica['consumer'].start()

    # Simula a falha de uma das replicas
    print("\nThere are {} replicas running.\n".format(len(replicas)))
    print("\nSimulating failure...\n")
    failed_replica = replicas.pop(1)
    failed_replica['monitor'].stop()
    failed_replica['consumer'].stop()
    print("\nThere are {} replicas running.\n".format(len(replicas)))

    # Para os monitores de sensores
    print("\nStopping remaining replicas in 5 seconds...\n")
    for replica in replicas:
        replica['monitor'].stop()
        replica['consumer'].stop()
    time.sleep(5)

    print("Done.")
