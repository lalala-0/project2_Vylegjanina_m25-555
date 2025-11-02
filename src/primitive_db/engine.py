import shlex
import prompt
from prettytable import PrettyTable

from src.primitive_db.utils import *
import src.primitive_db.core as core 
import src.primitive_db.parser as pars

META_PATH = "./data/db_meta.json"

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print_help()
    metadata = load_metadata(META_PATH)

    while True:
        try:
            user_input = prompt.string(">>>Введите команду: ")
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы...")
            break
        args = shlex.split(user_input) # pyright: ignore[reportArgumentType]
        cmd, *params = args

        try:

            match cmd:
                case "create_table":

                    core.create_table(metadata, params[0], params[1:])
                    save_metadata(META_PATH, metadata)
                case "drop_table":
                    core.drop_table(metadata, params[0])
                    save_metadata(META_PATH, metadata)
                case "list_tables":
                    core.list_tables(metadata)

                case "insert":
                    parsed = pars.parse_insert(params)
                    table_name = parsed["table"]
                    table_data = load_table_data(table_name)
                    new_data = core.insert(metadata, table_name, parsed["values"])
                    save_table_data(table_name, new_data)

                case "select":
                    parsed = pars.parse_select(params)
                    table_data = load_table_data(parsed["table"])
                    result = core.select(table_data, parsed["where"])
                    if not result:
                        print("Нет данных по запросу.")
                    else:
                        table = PrettyTable(result[0].keys())
                        for row in result:
                            table.add_row(row.values())
                        print(table)

                case "update":
                    parsed = pars.parse_update(params)
                    table_data = load_table_data(parsed["table"])
                    new_data = core.update(table_data, parsed["set"], parsed["where"])
                    save_table_data(parsed["table"], new_data)

                case "delete":
                    parsed = pars.parse_delete(params)
                    table_data = load_table_data(parsed["table"])
                    new_data = core.delete(table_data, parsed["where"])
                    save_table_data(parsed["table"], new_data)

                case "info":
                    parsed = pars.parse_info(params)
                    core.info(metadata, parsed["table"])


                case "help":
                    print_help()
                case "exit":
                    print("Завершение работы...")
                    break
                case _:
                    print(f"Неизвестная команда: {cmd}\n")
        except Exception as e:
            print(f"Ошибка: {e}")
            continue