from typing import Dict, Any, List
from src.primitive_db.utils import load_table_data, save_table_data

VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata: Dict[str, Dict[str, Dict[str, str]]], name: str, columns: Dict[str, str]) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Создаёт таблицу с колонками. Добавляет ID:int."""
    if name in metadata:
        print(f'Ошибка: Таблица "{name}" уже существует.')
        return metadata

    col_dict = {}
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        col_name, col_type = col.split(":")
        if col_type not in VALID_TYPES:
            print(f"Недопустимый тип: {col_type}")
            return metadata
        if col_name in col_dict:
            print(f"Ошибка: столбец {col_name} повторяется")
            return metadata
        col_dict[col_name] = col_type

    col_dict = {"ID": "int", **col_dict}
    metadata[name] = {"columns": col_dict}
    print(f'Tаблица "{name}" создана со столбцами: {", ".join(col_dict.keys())}')
    return metadata

def drop_table(metadata: Dict[str, Dict[str, Dict[str, str]]], name: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Удаляет таблицу."""
    if name not in metadata:
        print(f'Ошибка: Таблица "{name}" не найдена.')
        return metadata
    del metadata[name]
    print(f'Таблица "{name}" успешно удалена.')
    return metadata

def list_tables(metadata: Dict[str, Dict[str, Dict[str, str]]]) -> None:
    """Выводит метаданные всех таблиц."""
    if not metadata:
        print("Таблицы отсутствуют.")
        return
    print("Существующие таблицы:")
    for t in metadata:
        print("-", t)

def insert(metadata: Dict[str, Dict[str, Dict[str, str]]], table_name: str, values: List[Any]) -> None:
    """Вставляет запись в таблицу."""
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена.")
    schema = metadata[table_name]["columns"].copy()
    schema.pop("ID")

    if len(values) != len(schema):
        raise ValueError("Количество значений не совпадает со схемой таблицы.")

    validated = {}
    try:
        for (col, col_type), val in zip(schema.items(), values):
            if col_type == "int":
                if not isinstance(val, int):
                    raise ValueError(f"Ошибка: значение для столбца '{col}' должно быть целым числом.")
            elif col_type == "bool":
                if not isinstance(val, bool):
                    raise ValueError(f"Ошибка: значение для столбца '{col}' должно быть булевым (True/False).")
            elif col_type == "str":
                if not isinstance(val, str):
                    raise ValueError(f"Ошибка: значение для столбца '{col}' должно быть строкой.")
    except ValueError as e:
        raise ValueError(e)

    data = load_table_data(table_name)
    new_id = (len(data) + 1)
    validated["ID"] = new_id
    data.append(validated)
    save_table_data(table_name, data)
    print(f"Запись с ID={new_id} успешно добавлена в таблицу '{table_name}'.")

def select(table_data: List[Dict[str, Any]], where_clause: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
    """Выбирает записи из таблицы по условию WHERE, если условия нет - возвращает все данные таблицы."""
    if where_clause is {}:
        return table_data

    key, expected_value = where_clause.items()
    filtered = []
    for record in table_data:
        if key not in record:
            raise KeyError(f"Столбца '{key}' нет в таблице.")
        if str(record[key]) == expected_value:
            filtered.append(record)
    return filtered

def update(table_data: List[Dict[str, Any]], set_clause: Dict[str, Any], where_clause: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Обновляет записи в таблице по условию WHERE."""
    key_where, expected_value = where_clause
    key_set, new_value = set_clause
    updated_count = 0

    for record in table_data:
        if key_where not in record:
            raise KeyError(f"Столбца '{key_where}' нет в таблице.")
        if str(record[key_where]) == expected_value:
            if key_set not in record:
                raise KeyError(f"Столбеца '{key_set}' нет в таблице.")
            record[key_set] = new_value
            updated_count += 1

    print(f"Обновлено записей: {updated_count}")
    return table_data

def delete(table_data: List[Dict[str, Any]], where_clause: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Удаляет записи из таблицы по условию WHERE."""
    key, expected_value = where_clause
    initial_count = len(table_data)
    table_data = [record for record in table_data if str(record.get(key)) != expected_value]
    deleted_count = initial_count - len(table_data)

    print(f"Удалено записей: {deleted_count}")
    return table_data

def info(metadata: Dict[str, Dict[str, Dict[str, str]]], table_name: str) -> None:
    """Выводит информацию о таблице."""
    if table_name not in metadata:
        print("Таблица не найдена.")
        return
    schema = metadata[table_name]["columns"]
    table_data = load_table_data(table_name)
    print(f"Таблица: {table_name}")
    cols = ", ".join(f"{name}:{type_}" for name, type_ in schema.items())
    print(f"Столбцы: {cols}")
    print(f"Количество записей: {len(table_data)}")
