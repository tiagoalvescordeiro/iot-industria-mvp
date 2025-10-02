import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "iot")
DB_USER = os.getenv("DB_USER", "iot_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iot_pass")

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest():
    data = request.get_json(force=True)
    # Expect: sensor_id, timestamp, temperature (target is optional)
    sensor_id = int(data.get("sensor_id", 0))
    ts = float(data.get("timestamp"))
    temperature = float(data.get("temperature"))
    target = data.get("target", None)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO readings (sensor_id, timestamp, temperature, target) "
            "VALUES (to_number(%s, '999999'), to_timestamp(%s), %s, %s)",
            [sensor_id, ts, temperature, target]
        )
    return jsonify({"ok": True}), 201

@app.get("/readings")
def readings():
    limit = int(request.args.get("limit", 100))
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM readings ORDER BY timestamp DESC LIMIT %s",
            [limit]
        )
        rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    bind = os.getenv("INGEST_BIND", "0.0.0.0")
    port = int(os.getenv("INGEST_PORT", "5000"))
    app.run(host=bind, port=port)
