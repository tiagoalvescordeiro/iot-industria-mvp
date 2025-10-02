import os, time, random, json
from paho.mqtt import client as mqtt

BROKER = os.getenv("MQTT_BROKER_HOST", "localhost")
PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "iot/fase4/readings")

def main():
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.connect(BROKER, PORT, 60)
    c.loop_start()
    try:
        while True:
            payload = {
                "sensor_id": 1,
                "timestamp": time.time(),
                "temperature": round(random.uniform(18, 35), 2),
                "target": round(random.uniform(18, 35), 2)
            }
            c.publish(TOPIC, json.dumps(payload), qos=0, retain=False)
            print("Published:", payload)
            time.sleep(5)
    finally:
        c.loop_stop()

if __name__ == "__main__":
    main()
