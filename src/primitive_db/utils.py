import json
import os

from primitive_db.constants import DATA_DIR


def get_table_path(table_name):
    """Возвращает путь к JSON-файлу с данными таблицы."""

    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла (пустой словарь, если файла нет)."""

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    """Загружает записи таблицы (пустой список, если файла нет)."""

    try:
        with open(get_table_path(table_name), "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в JSON-файл в папке данных."""

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(get_table_path(table_name), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)