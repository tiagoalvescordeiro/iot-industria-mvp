import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST","localhost"),
    port=os.getenv("DB_PORT","5432"),
    dbname=os.getenv("DB_NAME","iot"),
    user=os.getenv("DB_USER","iot_user"),
    password=os.getenv("DB_PASSWORD","iot_pass"),
)
conn.autocommit = True
cur = conn.cursor()

with open("db/create_tables.sql","r") as f:
    cur.execute(f.read())

print("✅ Tabelas criadas.")

with open("db/load_sample_data.sql","r") as f:
    cur.execute(f.read())

print("✅ Dados de exemplo carregados.")
cur.close()
conn.close()
