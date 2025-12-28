import random
from datetime import datetime
from paho.mqtt import client as mqtt_client


BROKER = "mqtt-dashboard.com"
PORT = 8884  # TLS-port
TOPIC = "hajo66/devices/node1/up"
CLIENT_ID = f"python-mqtt-tcp-sub-{random.randint(0, 1000)}"  

def connect_mqtt():
    """
    Skapar och ansluter MQTT-klienten.
    """
    def on_connect(client, userdata, flags, rc):
        """
        Callback för att hantera anslutning till MQTT-broker.
        """
        if rc == 0:
            print(f"Ansluten till MQTT-broker: {BROKER} på port {PORT}")
            print(f"Prenumererar på topic: {TOPIC}")
            print("Väntar på meddelanden...\n")
        else:
            print(f"Misslyckades att ansluta, felkod: {rc}")

    client = mqtt_client.Client(CLIENT_ID)

    # Aktivera TLS/SSL
    print("Aktiverar TLS/SSL...")
    client.tls_set()  # För certifikatfria anslutningar
    

    client.on_connect = on_connect
    client.connect(BROKER, PORT, keepalive=60)
    return client

def subscribe(client: mqtt_client):
    """
    Prenumererar på ett topic och hanterar inkommande meddelanden.
    """
    def on_message(client, userdata, msg):
        """
        Callback för att hantera mottagna meddelanden.
        """
        try:
            now = datetime.now()
            dt = now.strftime("%Y-%m-%d %H:%M:%S")
            payload = msg.payload.decode()
            print(f"Mottaget ämne: {msg.topic}")
            print(f"Payload: {payload}")
            print(f"Mottaget vid lokal tid: {dt}\n")
        except Exception as e:
            print(f"Fel vid bearbetning av meddelande: {e}")

    client.subscribe(TOPIC)
    client.on_message = on_message

def run():
    """
    Startar MQTT-klienten och initierar prenumeration.
    """
    client = connect_mqtt()
    subscribe(client)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nAvslutar MQTT-prenumeration.")
        client.loop_stop()

if __name__ == "__main__":
    run()
