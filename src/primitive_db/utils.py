import json

def load_metadata(filepath):
    """Загружает метаданные базы."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Ошибка: поврежден json-файл метаданных, загружаю пустую БД")

def save_metadata(filepath, data):
    """Сохраняет метаданные базы. Возвращает True/False."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except IOError as e:
        raise IOError(f"Ошибка при сохранении в файл {filepath}: {e}")

def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла"""
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Ошибка: поврежден json-файл данных таблицы {table_name}, загружаю пустую таблицу")

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл. Возвращает True/False."""
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except IOError as e:
        raise IOError(f"Ошибка при сохранении в файл {filepath}: {e}")
