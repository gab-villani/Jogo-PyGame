import paho.mqtt.client as mqtt

server = 'localhost'
port = 1883

pos = [(0, 0), (100, 100)]

def on_connect(client, userdata, flags, rc):
    print("Conectado com código de resultado " + str(rc))
    client.subscribe("pos_topic")

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

def on_message(client, userdata, msg):
    global pos
    data = msg.payload.decode()
    pos = read_pos(data)
    print('Received:', data)
    print('Position:', pos)

def run_server():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(server, port, 60)
    client.loop_forever()

if __name__ == "__main__":
    run_server()
