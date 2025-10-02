import os
import streamlit as st
import pandas as pd
import psycopg2
import pickle
from dotenv import load_dotenv

load_dotenv()
THRESHOLD = float(os.getenv("THRESHOLD_TEMP", "45.0"))

@st.cache_data(ttl=30)
def get_df(limit=300):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST","localhost"),
        port=os.getenv("DB_PORT","5432"),
        dbname=os.getenv("DB_NAME","iot"),
        user=os.getenv("DB_USER","iot_user"),
        password=os.getenv("DB_PASSWORD","iot_pass"),
    )
    df = pd.read_sql(f"SELECT * FROM readings ORDER BY timestamp DESC LIMIT {limit}", conn)
    conn.close()
    return df

st.title("MVP Indústria 4.0 — KPIs & Alertas")
df = get_df()

col1, col2, col3 = st.columns(3)
col1.metric("Qtd Leituras", len(df))
col2.metric("Temp Média", f"{df['temperature'].mean():.2f} °C")
col3.metric("Temp Máx", f"{df['temperature'].max():.2f} °C")

st.subheader("Temperatura (últimas leituras)")
st.line_chart(df.sort_values("timestamp")[["timestamp","temperature"]].set_index("timestamp"))

# Inference (se modelo existir)
model_path = "ml/model.pkl"
if os.path.exists(model_path):
    with open(model_path,"rb") as f:
        model = pickle.load(f)
    preds = model.predict(df[["temperature"]].values)
    st.subheader("Previsão vs. Real (target)")
    if "target" in df.columns and df["target"].notna().any():
        comp = pd.DataFrame({"target": df["target"].values, "pred": preds}, index=df["timestamp"])
        st.line_chart(comp.sort_index())
        mae = (comp["target"] - comp["pred"]).abs().mean()
        st.metric("MAE (amostra)", f"{mae:.3f}")
    else:
        st.info("Sem 'target' suficiente para avaliar o modelo.")
else:
    st.warning("Modelo não encontrado. Treine em `ml/train_or_predict.py --mode train`.")

# Alertas por threshold
latest_temp = float(df["temperature"].iloc[0]) if len(df) else None
if latest_temp is not None and latest_temp > THRESHOLD:
    st.error(f"⚠️ Alerta: Temperatura {latest_temp:.2f} °C acima do threshold ({THRESHOLD:.1f} °C)")
else:
    st.success(f"✅ Dentro do limite ({THRESHOLD:.1f} °C)")

st.caption("Atualiza a cada 30s (cache). Ajuste THRESHOLD_TEMP no .env.")
