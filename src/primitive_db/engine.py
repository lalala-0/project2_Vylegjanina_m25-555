import prompt


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        try:
            user_input = prompt.string("Введите команду: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы...")
            break

        match user_input:
            case "help":
                print("\n<command> exit - выйти из программы")
                print("<command> help - справочная информация")
            case "exit":
                print("Завершение работы...")
                break
            case _:
                print(f"Неизвестная команда: {user_input}\n")
