import time
from functools import wraps


def handle_db_errors(func):
    """
    Декоратор для централизованной обработки ошибок, возникающих при работе с БД.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Ошибка, файл не найден: {e}")
        except KeyError as e:
            print(f"Ошибка, ключ не найден: {e}")
        except ValueError as e:
            print(f"Ошибка, некорректное значение: {e}")
        except IOError as e:
            print(f"Ошибка ввода-вывода: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")
    return wrapper


def confirm_action(act_name):
    """
    Декоратор-фабрика, запрашивающий подтверждение у пользователя для опасных операций.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, '\
                        f'что хотите выполнить "{act_name}"? [y/n]: ').strip().lower()
            if answer == 'y':
                return func(*args, **kwargs)
            print("Операция отменена пользователем.")
        return wrapper
    return decorator


def log_time(func):
    """
    Декоратор для измерения времени выполнения функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        duration = time.monotonic() - start
        print(f"Функция {func.__name__} выполнилась за {duration:.3f} секунд.")
        return result
    return wrapper


def create_cacher():
    """
    Возвращает функцию, реализующую кэширование результатов для select.
    """
    cache_storage = {}

    def cache_result(key, value_func):
        if key in cache_storage:
            print(f"Результат для {key} взят из кэша")
            return cache_storage[key]
        value = value_func()
        cache_storage[key] = value
        return value

    return cache_result
