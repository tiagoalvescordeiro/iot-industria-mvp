import os, time, random, requests, json
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://api:5000/ingest")

def main():
    while True:
        payload = {
            "sensor_id": 1,
            "timestamp": time.time(),
            "temperature": round(random.uniform(18, 35), 2),
            "target": round(random.uniform(18, 35), 2)
        }
        r = requests.post(API_URL, json=payload, timeout=5)
        print("Enviado:", payload, "status:", r.status_code)
        time.sleep(5)

if __name__ == "__main__":
    main()
