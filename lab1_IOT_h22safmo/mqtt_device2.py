import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt


BROKER = "mqtt-dashboard.com"
PORT = 8884
CLIENT_ID = "BqGE3of9m7"  #klient-ID
TOPIC_UP = "hajo66/devices/node1/up"
TOPIC_DOWN = "hajo66/devices/node1/down"

# Funktion för anslutning
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Ansluten till broker: {BROKER} med Client ID: {CLIENT_ID}")
        client.subscribe(TOPIC_UP)  # Prenumerera på upp-ämnet
        print(f"Prenumererar på topic: {TOPIC_UP}")
    else:
        print(f"Anslutning misslyckades, kod: {rc}")

# Funktion för att ta emot meddelanden
def on_message(client, userdata, msg):
    local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = msg.payload.decode()
    print(f"Mottaget ämne: {msg.topic} med payload: '{payload}' vid lokal tid: {local_time}")

    try:
        # Försök att analysera JSON-payload
        data = json.loads(payload)
        print(f"Valid JSON: {data}")
        ack_message = "ACK_MSG_RECEIVED"
        print(f"Publicerar till {TOPIC_DOWN}: {ack_message}")
        client.publish(TOPIC_DOWN, ack_message, qos=1)  # Använd QoS 1 för garanterad leverans
        print(f"Message ID: {data.get('message id/counter', 'N/A')}\n")
    except json.JSONDecodeError:
        print("Felaktig JSON mottagen.\n")

# Funktion för att skapa och skicka data
def generate_data():
    sensor_data = {
        "app_id": "hajo66",
        "dev_id": "node1",
        "temperature": random.randint(0, 70),
        "humidity": random.randint(10, 90),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message id/counter": random.randint(1, 1000)
    }
    return json.dumps(sensor_data)

# Anslut och kör MQTT-klienten
def run_mqtt():
    # Skapa MQTT-klienten med specifik Client ID
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    # Aktivera TLS/SSL
    print("Konfigurerar TLS/SSL...")
    client.tls_set()  # Om inga certifikat krävs, räcker det med detta
    # För specifika certifikat:

    print("Ansluter till broker...")
    client.connect(BROKER, PORT, 60)  # Port 8884 för TLS
    client.loop_start()  # Starta loop för att hantera meddelanden

    while True:
        # Generera och publicera sensor data
        data = generate_data()
        print(f"Publicerar till {TOPIC_UP}: {data}")
        client.publish(TOPIC_UP, data, qos=1)  # Använd QoS 1

        time.sleep(5)  # Vänta innan nästa publicering

if __name__ == "__main__":
    run_mqtt()
