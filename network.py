import paho.mqtt.client as mqtt
import time

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

class Network:
    def __init__(self):
        self.client = mqtt.Client()
        self.server = 'localhost'
        self.port = 1883
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com código de resultado " + str(rc))

    def on_disconnect(self, client, userdata, rc):
        print("Desconectado com código de resultado " + str(rc))

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        self.pos = read_pos(data)
        print('Received:', data)
        print('Position:', self.pos)

    def connect(self):
        try:
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            self.client.connect(self.server, self.port, 60)
            self.client.subscribe("pos_topic")
            self.client.loop_start()
            return (0, 0)
        except Exception as e:
            print(e)
            return (0, 0)

    def send(self, data):
        try:
            self.client.publish("pos_topic", make_pos(data))
            time.sleep(0.1)  # Aguarde um curto período para permitir a recepção da mensagem
            return self.pos
        except Exception as e:
            print(e)
            return (0, 0)

if __name__ == "__main__":
    net = Network()
