import os, json, requests
from paho.mqtt import client as mqtt

BROKER = os.getenv("MQTT_BROKER_HOST", "localhost")
PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "iot/fase4/readings")
API_URL = os.getenv("API_URL", "http://api:5000/ingest")

def on_connect(client, userdata, flags, rc, props=None):
    print("Connected to MQTT with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        r = requests.post(API_URL, json=payload, timeout=5)
        print("Bridged:", payload, "status:", r.status_code)
    except Exception as e:
        print("Bridge error:", e)

def main():
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.on_connect = on_connect
    c.on_message = on_message
    c.connect(BROKER, PORT, 60)
    c.loop_forever()

if __name__ == "__main__":
    main()
