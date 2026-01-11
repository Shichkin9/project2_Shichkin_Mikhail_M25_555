import json
from pathlib import Path

DATA_DIR = "src/primitive_db/data"

def load_metadata(filepath: Path):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath: Path, data: dict):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_table_data(table_name):
    """Загрузка данных таблицы из JSON"""
    filepath = Path(DATA_DIR) / f"{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """Сохранение данных таблицы в JSON"""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    filepath = Path(DATA_DIR) / f"{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
