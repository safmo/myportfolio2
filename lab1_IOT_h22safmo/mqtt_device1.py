import json
import random
import time
from datetime import datetime
from paho.mqtt import client as mqtt_client

BROKER = "mqtt-dashboard.com"
PORT = 8884  # TLS/SSL port
TOPIC_UP = "hajo66/devices/node1/up"
CLIENT_ID = f"python-mqtt-tcp-pub-{random.randint(0, 1000)}"

FLAG_CONNECTED = 0  # för att spåra anslutningsstatus


def on_connect(client, userdata, flags, rc):
    """Anropas vid anslutning till MQTT-brokern."""
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print(f"Ansluten till broker: {BROKER} på port {PORT}")
        print(f"Publicerar till topic: {TOPIC_UP}\n")
    else:
        print(f"Misslyckades att ansluta, felkod: {rc}")


def connect_mqtt():
    """Skapar och ansluter MQTT-klienten."""
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect

    # Aktivera TLS/SSL
    print("Aktiverar TLS/SSL...")
    client.tls_set()  # För certifikatfria anslutningar
    # För specifika certifikat, använd följande:
    # client.tls_set(ca_certs="ca.crt", certfile="client.crt", keyfile="client.key")

    client.connect(BROKER, PORT, keepalive=60)
    return client


def generate_sensor_data(msg_count):
    """Genererar slumpmässig sensordata."""
    return {
        "app_id": "hajo66",
        "dev_id": "nodel",
        "port/channel": random.randint(1, 100),
        "rssi": random.randint(-100, 1),
        "snr": random.randint(-50, 100),
        "sf": "SF7BW125",
        "C_F": "C",
        "Tempeture": random.randint(0, 70),
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message id/counter": msg_count,
    }


def main():
    """Huvudfunktion som ansluter och skickar data."""
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)  # Vänta på att anslutningen ska slutföras

    msg_count = 1
    while True:
        try:
            # Generera sensordata
            data = generate_sensor_data(msg_count)
            js_data = json.dumps(data)

            # Publicera data
            result = client.publish(TOPIC_UP, js_data, qos=1)
            status = result[0]
            if status == 0:
                print(f"Sensor data: {data['Tempeture']}°C, Time: {data['Time']}, Message ID: {data['message id/counter']}")
                print(f"Publicerar till {TOPIC_UP}, JSON payload: {js_data}\n")
            else:
                print(f"Misslyckades att publicera till {TOPIC_UP}")

            msg_count += 1
            time.sleep(1)  # Publicera data varje sekund

        except KeyboardInterrupt:
            print("\nAvslutar anslutning...")
            client.loop_stop()
            break


if __name__ == "__main__":
    main()
