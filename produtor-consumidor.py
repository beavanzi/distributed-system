# Academica: Beatriz Avanzi Ecli        RA: 108612

# O código implementa o padrão produtor-consumidor, onde o produtor é a classe SensorMonitor e o consumidor é a classe MessageBroker. 
# O objetivo é simular a leitura de sensores e publicar os valores lidos em uma fila de mensagens para que o consumidor possa consumi-las.
# O produtor, SensorMonitor, é responsável por ler os valores dos sensores em um loop e publicá-los na fila de mensagens 
# através do método publish do objeto MessageBroker. A cada leitura do sensor, o produtor cria uma mensagem com o 
# nome do sensor e o valor lido, e publica essa mensagem na fila.
# O consumidor, MessageBroker, é responsável por consumir as mensagens publicadas na fila de mensagens através do método consume. 
# Esse método é executado em um loop infinito, onde a cada iteração ele tenta obter uma mensagem da fila. 
# Se uma mensagem estiver disponível, ele a consome e a exibe na saída padrão.
# No código, o produtor é iniciado primeiro, seguido pelo consumidor. O produtor é executado por 10 segundos e, em seguida, é parado. 
# O consumidor é executado em um loop infinito, mas como a fila é esvaziada quando o produtor é parado, o consumidor eventualmente detecta 
# que a fila está vazia e bloqueia até que uma nova mensagem seja publicada na fila. Quando o produtor é parado, o consumidor imprime "Execution Done." 
# e o programa termina.


import random
import socket
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

    def add_connection(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.connections.append(s)

    def publish(self, message):
        self.queue.put(message)

    def consume(self):
        while True:
            try:
                message = self.queue.get(timeout=1)
                print(f"Consumed message: {message}")
            except queue.Empty:
                if not monitor.running and self.queue.empty():
                    break

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
            for sensor in self.sensors:
                value = sensor.read()
                message = f"{sensor.name}:{value}"
                self.message_broker.publish(message)
            time.sleep(1)

if __name__ == "__main__":

    # Cria os sensores
    sensors = [Sensor(f"Sensor-{i}") for i in range(5)]

    # Cria o message broker
    message_broker = MessageBroker()

    # Cria o monitor de sensores
    monitor = SensorMonitor(sensors, message_broker)

    # Inicia o monitor de sensores
    monitor.start()
    
    # Cria o consumidor de mensagens
    consumer = threading.Thread(target=message_broker.consume)
    consumer.start()

    # Aguarda o monitor de sensores por 10 segundos
    time.sleep(10)

    # Para o monitor de sensores
    monitor.stop()

    # Aguarda o consumidor de mensagens
    consumer.join()

    print("Execution done.")