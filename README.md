
# 💡 MVP IoT Industrial - Hermes Reply

Este projeto integra sensores (ESP32/simulação), ingestão de dados, persistência em banco relacional, aplicação de Machine Learning e visualização com alertas, consolidando as entregas anteriores em um pipeline fim-a-fim.

## 📁 Estrutura do Repositório

```
📦iot-industria-mvp/
 ┣ 📂api/              → Backend básico com endpoints de ingestão (simulado)
 ┣ 📂db/               → Scripts SQL de criação e carga de banco de dados
 ┣ 📂ml/               → Notebooks e scripts de Machine Learning
 ┣ 📂mqtt/             → Lógica de simulação/ingestão via MQTT (com ESP32 ou mock)
 ┣ 📂dashboard/        → Aplicação de dashboard (ex: Streamlit)
 ┣ 📂docs/             → Diagrama de arquitetura (.drawio/.png)
 ┣ 📜README.md         → Instruções do projeto
```

## 🚀 Execução

1. **Ingestão**: simulação com sensor ESP32 ou mock → `/mqtt`
2. **Carga no Banco**: scripts SQL → `/db`
3. **ML**: notebook com inferência e visualização → `/ml`
4. **Dashboard**: Streamlit ou notebook com alertas → `/dashboard`

## 📊 Tecnologias

- ESP32 (Wokwi ou PlatformIO)
- Python (pandas, scikit-learn, matplotlib)
- SQLite / MySQL
- Streamlit / Dash
- MQTT / HTTP (simulado)

## 🧠 Decisões Técnicas

- Utilização de thresholds simples para alertas
- Inferência por batch para facilitar reprodutibilidade
- Dados persistidos com integridade relacional
- Visualizações construídas em notebook e app leve

## 📺 Demonstração (YouTube)

[Inserir link do vídeo não listado]

## 👥 Equipe

Este projeto foi desenvolvido como parte do desafio Hermes Reply — Sprint 3 do curso de Engenharia de Software.

**Integrantes:**

- Otávio Custódio — RM: 565606  
- Matheus Parra — RM: 561907  
- Tiago Alves Cordeiro — RM: 561791  
- Thiago Henrique Pereira de Almeida Santos — RM: 563327  
- Leandro Arthur Marinho Ferreira — RM: 565240

🔗 [Acesse o repositório oficial no GitHub](https://github.com/tiagoalvescordeiro/Enterprise-Challenge—Sprint-3—Reply)

docker compose up -d --build
```
2) Inicie o **bridge** (subscritor) automaticamente pelo compose e publique leituras de teste:
```bash
docker compose exec api python scripts/mqtt_publisher.py
```
> O bridge (serviço `mqtt_bridge`) recebe mensagens em `iot/fase4/readings` e envia para `POST /ingest` da API.

## Notebook de ML
- Execute `ml/analysis.ipynb` (VSCode, Jupyter, ou dentro do container `api` se preferir). Ele treina um RandomForest e imprime o **MAE** + gráfico.
