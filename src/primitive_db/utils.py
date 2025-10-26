import json

def load_metadata(filepath):
    """Загружает метаданные базы."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Ошибка: поврежден json-файл метаданных, загружаю пустую БД")
        return {}

def save_metadata(filepath, data):
    """Сохраняет метаданные базы. Возвращает True/False."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return True
    except IOError as e:
        print(f"Ошибка при сохранении в файл {filepath}: {e}")
        return False
