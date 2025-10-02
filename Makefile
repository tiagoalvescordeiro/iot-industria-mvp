SHELL := /bin/bash

.PHONY: up down rebuild init sender mqtt ml dash logs test lint ci

up:
	docker compose up -d --build

down:
	docker compose down -v

rebuild: down up

init:
	docker compose exec api python scripts/init_db.py

sender:
	docker compose exec api python scripts/sender.py

mqtt:
	docker compose exec api python scripts/mqtt_publisher.py

ml:
	docker compose exec api python ml/train_or_predict.py --mode train

dash:
	@echo "Dashboard em http://localhost:8501"

logs:
	docker compose logs -f --tail=100

lint:
	flake8 .

test:
	pytest

ci: lint test
