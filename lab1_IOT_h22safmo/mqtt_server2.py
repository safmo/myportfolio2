import json
import random
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client

BROKER = "mqtt-dashboard.com"
PORT = 8884  # TLS-port
TOPIC_UP = "hajo66/devices/node1/up"
TOPIC_DOWN = "hajo66/devices/node1/down"
CLIENT_ID = f"python-mqtt-server-{random.randint(0, 1000)}"  # Dynamisk klient-ID

# Flagga för att spåra anslutningsstatus
FLAG_CONNECTED = 0

def on_message(client, userdata, msg):
    """
    Callback för att hantera mottagna meddelanden.
    """
    try:
        # Logga mottagna meddelanden
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        payload = msg.payload.decode()
        print(f"Mottaget ämne: {msg.topic} med payload: {payload}")
        print(f"Mottaget vid lokal tid: {dt}\n")
        
        # Skicka ACK tillbaka till enheten
        ack_data = {
            'app_id': 'hajo66', 
            'dev_id': 'node1', 
            'message': 'ACK_MSG_RECEIVED',
            'Time': dt
        }
        ack_json = json.dumps(ack_data, default=str)
        client.publish(TOPIC_DOWN, ack_json)
        print(f"Skickat ACK: {ack_json}\n")
    except Exception as e:
        print(f"Fel vid bearbetning av meddelande: {e}")

def on_connect(client, userdata, flags, rc):
    """
    Callback för att hantera anslutning till MQTT-broker.
    """
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print(f"Ansluten till MQTT-broker: {BROKER} på port {PORT}")
        print(f"Prenumererar på topic: {TOPIC_UP}")
        print("Väntar på meddelanden...\n")
        client.subscribe(TOPIC_UP)
    else:
        print(f"Misslyckades att ansluta, felkod: {rc}")

def connect_mqtt():
    """
    Skapar och ansluter MQTT-klienten.
    """
    client = mqtt_client.Client(CLIENT_ID)

    # Aktivera TLS/SSL
    print("Aktiverar TLS/SSL för säker anslutning...")
    client.tls_set()  # Använd standardinställningar för TLS/SSL

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    return client

def run():
    """
    Startar MQTT-server och håller den igång för att hantera meddelanden.
    """
    client = connect_mqtt()
    client.loop_start()  # Startar klientens loop i en separat tråd

    try:
        while True:
            time.sleep(5)  # Håller servern igång
    except KeyboardInterrupt:
        print("\nAvslutar MQTT-server...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run()
