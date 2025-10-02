import os, pytest

def test_required_directories_exist():
    required = [
        "api", "db", "ml", "dashboard", "docs/arquitetura", "scripts", ".github/workflows"
    ]
    for r in required:
        assert os.path.isdir(r), f"Missing directory: {r}"

def test_required_files_exist():
    files = [
        "db/create_tables.sql",
        "api/app.py",
        "dashboard/app.py",
        "ml/train_or_predict.py",
        "docker-compose.yml",
        "requirements.txt",
        "README.md"
    ]
    for f in files:
        assert os.path.exists(f), f"Missing file: {f}"
