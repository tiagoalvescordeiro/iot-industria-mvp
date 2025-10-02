import argparse, os, pickle
import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from dotenv import load_dotenv

load_dotenv()

def load_df(limit=1000):
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

def train():
    df = load_df(2000)
    df = df.dropna(subset=["temperature", "target"])
    X = df[["temperature"]].values
    y = df["target"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    print(f"MAE: {mae:.4f}")
    with open("ml/model.pkl","wb") as f:
        pickle.dump(model, f)
    return mae

def infer(temp_values):
    with open("ml/model.pkl","rb") as f:
        model = pickle.load(f)
    return model.predict(temp_values)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["train","infer"], default="train")
    args = p.parse_args()
    if args.mode == "train":
        train()
    else:
        import numpy as np
        print(infer(np.array([[25.0],[30.0]])))
