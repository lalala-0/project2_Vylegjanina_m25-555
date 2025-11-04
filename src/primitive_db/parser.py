from typing import Any, Dict, List


def parse_value(value: str) -> Any:
    """
    Преобразует строку в значение нужного типа:
    - int, если это целое число;
    - bool, если 'true' или 'false';
    - str, если в кавычках.
    """
    value = value.strip()

    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Значение {value} недопустимого типа. Ожидается int, bool или строка в кавычках.")



def parse_insert(params: List[str]) -> Dict[str, Any]:
    """
    insert into <table> values (<v1>, <v2>, ...)
    Пример:
        ['into', 'users', 'values', '("Alice",', '25,', 'true)']
    """
    if len(params) < 4 or params[0] != "into" or params[2] != "values":
        raise ValueError("Неверный синтаксис insert. Ожидается: insert into <имя_таблицы> values (<значение1>, <значение2>, ...)")

    table = params[1]
    values_str = " ".join(params[3:]).strip("()")
    raw_values = [v.strip() for v in values_str.split(",") if v.strip()]

    parsed_values = [parse_value(v) for v in raw_values]
    return {"table": table, "values": parsed_values}


def parse_select(params: List[str]) -> Dict[str, Any]:
    """
    select from <table> [where <col> = <val>]
    Примеры:
        ['from', 'users']
        ['from', 'users', 'where', 'age', '=', '30']
    """
    if len(params) < 2 or params[0] != "from":
        raise ValueError("Неверный синтаксис select. Ожидается: select from <имя_таблицы> [where <столбец> = <значение>]")

    table = params[1]

    if len(params) > 2:
        if len(params) != 6 or params[2] != "where" or params[4] != "=":
            raise ValueError("Неверный синтаксис where. Ожидается: where <столбец> = <значение>")
        column = params[3]
        value = parse_value(params[5])
        return {"table": table, "where": {column: value}}

    return {"table": table, "where": None}


def parse_update(params: List[str]) -> Dict[str, Any]:
    """
    update <table> set <col> = <val> where <col> = <val>
    Пример:
        ['users', 'set', 'age', '=', '31', 'where', 'name', '=', '"Alice"']
    """
    if len(params) != 9 or params[1] != "set" or params[5] != "where" :
        raise ValueError("Неверный синтаксис update. " \
        "Ожидается: update <имя_таблицы> set <столбец_условия> = <значение_условия> where <столбец_условия> = <значение_условия>")

    table = params[0]
    where_idx = params.index("where")
    set_part = params[2:where_idx]
    where_part = params[where_idx + 1:]

    if len(set_part) != 3 or set_part[1] != "=":
        raise ValueError("Неверный синтаксис set. Ожидается: set<столбец_условия> = <значение_условия>")
    set_clause = {set_part[0]: parse_value(set_part[2])}

    if len(where_part) != 3 or where_part[1] != "=":
        raise ValueError("Неверный синтаксис where. Ожидается: where <столбец_условия> = <значение_условия>")
    where_clause = {where_part[0]: parse_value(where_part[2])}

    return {"table": table, "set": set_clause, "where": where_clause}


def parse_delete(params: List[str]) -> Dict[str, Any]:
    """
    delete from <имя_таблицы> where <col> = <val>
    Пример: ['from', 'users', 'where', 'age', '=', '40']
    """
    if len(params) != 6 or params[0] != "from" or params[2] != "where" or params[4] != "=":
        raise ValueError("Неверный синтаксис delete. Ожидается: delete from <имя_таблицы> where <столбец> = <значение> ")

    table = params[1]
    column = params[3]
    value = parse_value(params[5])
    return {"table": table, "where": {column: value}}


def parse_info(params: List[str]) -> Dict[str, Any]:
    """
    info <table>
    Пример: ['users']
    """
    if len(params) != 1:
        raise ValueError("Неверный синтаксис info. Ожидается: info <имя_таблицы>")
    return {"table": params[0]}
