"""Реализация декораторов и замыкания для кэширования"""

import functools
import time

import prompt


def handle_db_errors(func):
    """Декоратор для обработки ошибок базы данных"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return False, "Ошибка: Файл данных не найден. Возможно, база данных не инициализирована." 
        except KeyError as e:
            return False, f"Ошибка: Таблица или столбец {e} не найден."
        except ValueError as e:
            return False, f"Ошибка валидации: {e}"
        except Exception as e:
            return False, f"Произошла непредвиденная ошибка: {e}"
    return wrapper


def confirm_action(action_name):
    """Декоратор для подтверждения опасных операций"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            table_name = None
            if len(args) > 1:
                table_name = args[1] 
            
            if table_name:
                message = f'Вы уверены, что хотите выполнить "{action_name}" для таблицы "{table_name}"? [y/N]: ' 
            else:
                message = f'Вы уверены, что хотите выполнить "{action_name}"? [y/N]: '
            
            answer = prompt.string(message).strip().lower()
            
            if answer == 'y' or answer == 'yes':
                return func(*args, **kwargs)
            else:
                return False, f'Операция "{action_name}" отменена.'
        return wrapper
    return decorator


def log_time(func):
    """Декоратор для замера времени выполнения функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд.")
        return result
    return wrapper


def create_cacher():
    """Фабрика функций для кэширования результатов"""
    cache = {}
    
    def cache_result(key, value_func):
        """Внутренняя функция для кэширования"""
        if key in cache:
            print(f"Использован кэш для ключа: {key}")
            return cache[key]
        else:
            result = value_func()
            cache[key] = result
            print(f"Добавлено в кэш для ключа: {key}")
            return result
    
    def clear_cache():
        """Очистить кэш."""
        cache.clear()
        print("Кэш очищен.")
    
    def get_cache_stats():
        """Получить статистику кэша"""
        return {
            'size': len(cache),
            'keys': list(cache.keys())
        }
    
    # Возвращаю словарь с функциями
    return {
        'cache_result': cache_result,
        'clear_cache': clear_cache,
        'get_stats': get_cache_stats
    }
