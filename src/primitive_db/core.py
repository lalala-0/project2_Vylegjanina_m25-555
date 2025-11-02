VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata, name, columns):
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

def drop_table(metadata, name):
    """Удаляет таблицу."""
    if name not in metadata:
        print(f'Ошибка: Таблица "{name}" не найдена.')
        return metadata
    del metadata[name]
    print(f'Таблица "{name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    """Выводит метаданные всех таблиц."""
    if not metadata:
        print("Таблицы отсутствуют.")
        return
    print("Существующие таблицы:")
    for t in metadata:
        print("-", t)
