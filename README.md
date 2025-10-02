# MVP Indústria 4.0 — Hermes Reply Challenge

**Fluxo end-to-end (simulado):** ESP32/Sim → API (Flask) → PostgreSQL → ML (sklearn) → Dashboard (Streamlit) com alerta por _threshold_.

## Como rodar (opção 1: Docker Compose — recomendado)
1) Instale Docker e Docker Compose (v2+).
2) Copie `.env.example` para `.env` e ajuste se necessário.
3) Suba os serviços:
```bash
docker compose up -d --build
```
4) Crie as tabelas no PostgreSQL:
```bash
docker compose exec api python scripts/init_db.py
```
5) Inicie a ingestão simulada (gera leituras a cada 5s):
```bash
docker compose exec api python scripts/sender.py
```
6) (Opcional) Treine o modelo e gere `model.pkl`:
```bash
docker compose exec api python ml/train_or_predict.py --mode train
```
7) Abra o dashboard Streamlit (porta 8501):
- Acesse: http://localhost:8501

## Como rodar (opção 2: local)
Crie um _virtualenv_, instale `requirements.txt`, suba um PostgreSQL local e exporte as variáveis do `.env`. Rode:
```bash
python api/app.py
python scripts/init_db.py
python scripts/sender.py
streamlit run dashboard/app.py
```

## Pastas
- `docs/arquitetura/` — diagrama (.drawio placeholder) e PNG (adicione seu export do app.diagrams.net).
- `api/` — API Flask para ingestão e leitura.
- `db/` — scripts SQL.
- `ml/` — treino/inferência simples com sklearn.
- `dashboard/` — Streamlit com KPIs e alerta (threshold).
- `scripts/` — utilitários (init_db, sender simulado).
- `.github/workflows/` — CI (lint básico).

## Pipeline
1. **Ingestão:** `scripts/sender.py` envia JSON para `POST /ingest`.
2. **Armazenamento:** API insere no Postgres (`readings`).
3. **ML:** `ml/train_or_predict.py` lê do banco, treina modelo (RandomForestRegressor) e salva `model.pkl`.
4. **Visualização:** `dashboard/app.py` lê do banco, mostra KPIs e alerta quando `temperature > THRESHOLD`.

## Vídeo
Grave um vídeo de até 5 min mostrando: arquitetura → ingestão → banco → ML → dashboard/alerta. Publique como "não listado" no YouTube e inclua o link acima.


## Ingestao via MQTT (opcional)
1) Suba os serviços incluindo Mosquitto e o bridge:
```bash
docker compose up -d --build
```
2) Inicie o **bridge** (subscritor) automaticamente pelo compose e publique leituras de teste:
```bash
docker compose exec api python scripts/mqtt_publisher.py
```
> O bridge (serviço `mqtt_bridge`) recebe mensagens em `iot/fase4/readings` e envia para `POST /ingest` da API.

## Notebook de ML
- Execute `ml/analysis.ipynb` (VSCode, Jupyter, ou dentro do container `api` se preferir). Ele treina um RandomForest e imprime o **MAE** + gráfico.
