import json
import random
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client

BROKER = "mqtt-dashboard.com"
PORT = 8884
TOPIC_UP = "hajo66/devices/node1/up"
TOPIC_DOWN = "hajo66/devices/node1/down"
CLIENT_ID = "BqGE3of9m7"  #det klient-ID:t

FLAG_CONNECTED = 0

# Callback för anslutning
def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print(f"Connected to broker: {BROKER}")
        print(f"Connected to port: {PORT}")
        print(f"Publishing to topic: {TOPIC_UP}")
        print(f"Listening on topic: {TOPIC_DOWN}")
        print("Ready to send and receive messages...\n")
        client.subscribe(TOPIC_DOWN)  # Prenumerera på TOPIC_DOWN
    else:
        print(f"Failed to connect, return code {rc}")

# Callback för bortkoppling
def on_disconnect(client, userdata, rc):
    global FLAG_CONNECTED
    print(f"Disconnected with return code {rc}")
    FLAG_CONNECTED = 0
    while not FLAG_CONNECTED:
        try:
            print("Attempting to reconnect...")
            client.reconnect()
            print("Reconnected successfully.")
        except Exception as e:
            print(f"Reconnect failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Callback för inkommande meddelanden
def on_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}: {msg.payload.decode()}")

# Funktion för att ansluta MQTT-klienten
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Konfigurera TLS
    client.tls_set()  # Använder standardcertifikat
    client.tls_insecure_set(True)  # Tillåt osäkra certifikat
    client.connect(BROKER, PORT, keepalive=120)
    return client

# Anslut MQTT-klienten
client = connect_mqtt()
client.loop_start()
time.sleep(1)

msg_count = 1
while True:
    try:
        # Generera slumpmässiga sensorvärden
        tem = random.randint(0, 70)
        port_channel = random.randint(1, 100)
        rssi = random.randint(-100, 1)
        snr = random.randint(-50, 100)
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")

        data = {
            'app_id': 'hajo66',
            'dev_id': 'nodel',
            'port/channel': port_channel,
            'rssi': rssi,
            'snr': snr,
            'sf': 'SF7BW125',
            'C_F': 'C',
            'Tempeture': tem,
            'Time': dt,
            'message id/counter': msg_count,
        }
        js_data = json.dumps(data, default=str)

        # Publicera meddelandet
        result = client.publish(TOPIC_UP, js_data)
        status = result[0]
        if status == 0:
            print("Sensor data: {Tempeture}° C at time: {Time}  Message id: {message id/counter}".format(**data))
            print(f"Publishing to topic: {TOPIC_UP}, JSON payload: {js_data}\n")
        else:
            print(f"Failed to send message id {msg_count}, retrying...")
            client.reconnect()
            client.publish(TOPIC_UP, js_data)

        msg_count += 1
        client.loop(timeout=2.0)  # Hantera inkommande meddelanden
        time.sleep(5)  # Vänta innan nästa meddelande skickas

    except Exception as e:
        print(f"An error occurred: {e}. Retrying in 5 seconds...")
        time.sleep(5)
