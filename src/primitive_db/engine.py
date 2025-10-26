import shlex
import prompt

import src.primitive_db.core as core 
from src.primitive_db.utils import load_metadata, save_metadata

META_PATH = "./data/db_meta.json"

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
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

        match cmd:
            case "create_table":
                core.create_table(metadata, params[0], params[1:])
                save_metadata(META_PATH, metadata)
            case "drop_table":
                core.drop_table(metadata, params[0])
                save_metadata(META_PATH, metadata)
            case "list_tables":
                core.list_tables(metadata)
            case "help":
                print_help()
            case "exit":
                print("Завершение работы...")
                break
            case _:
                print(f"Неизвестная команда: {cmd}\n")
