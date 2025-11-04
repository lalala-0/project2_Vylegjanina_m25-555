import json


def load_metadata(filepath):
    """Загружает метаданные базы."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл метаданных {filepath} не найден: {e}.")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Поврежден json-файл метаданных {filepath}: {e}")

def save_metadata(filepath, data):
    """Сохраняет метаданные базы. Возвращает True/False."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except IOError as e:
        raise IOError(f"Ошибка при сохранении в файл {filepath}: {e}")

def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла"""
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return list()
        #raise FileNotFoundError(f"Файл данных таблицы {table_name} не найден: {e}")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filepath}: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Поврежден json-файл данных таблицы {table_name}: {e}", e)

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл. Возвращает True/False."""
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except IOError as e:
        raise IOError(f"Ошибка при сохранении в файл {filepath}: {e}")
