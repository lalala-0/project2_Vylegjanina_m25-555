def parse_value(value: str):
    """
    Разбирает пользовательский ввод и возвращает значение с правильным типом:
    - int, если введено целое число
    - bool, если 'true' или 'false'
    - str, если строка в кавычках
    """

    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)

    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    raise ValueError("Некорректное значение. Используйте число, true/false или строку в кавычках.")


def parse_condition(condition_str: str):
    """
    Преобразует параметры, введённые пользователем, в словарь.
    Наример: 'age = 28' -> {'age': 28}
    """
    if not condition_str:
        return None

    if "=" not in condition_str:
        raise ValueError("Ожидается выражение в формате 'поле = значение'")

    column, value_str = condition_str.split("=", 1)
    column = column.strip()
    value_str = value_str.strip()

    value = parse_value(value_str)

    return {column: value}
