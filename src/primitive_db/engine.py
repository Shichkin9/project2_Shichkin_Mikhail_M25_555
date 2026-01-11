# src/primitive_db/engine.py

import shlex
from pathlib import Path

from .core import (
    delete,
    info_table,
    insert,
    select,
    update,
)
from .utils import load_metadata, load_table_data, save_metadata, save_table_data

METADATA_FILE = Path("src/primitive_db/db_meta.json")
DATA_DIR = Path("src/primitive_db/data")
DATA_DIR.mkdir(exist_ok=True)


# Тут будут функции, которые будут нам помогать:) 

def parse_where_clause(where_str):
    """Превращает строчку вида 'age = 19' или 'name = "Mike"' в словарь {'age': 19}"""
    try:

        key, val = map(str.strip, where_str.split("=", 1))
        
        # Если значение в кавычках, оставляем как строку
        if ((val.startswith('"') and val.endswith('"')) or 
            (val.startswith("'") and val.endswith("'"))):
            val = val[1:-1]

        elif val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False

        else:
            try:
                val = int(val)
            except ValueError:
                val = val  
        return {key: val}
    except Exception:
        print(f"Некорректное условие: {where_str}")
        return None



def parse_values(values_str):
    """Превращает строку '"Mike", 19, true' в список ['Mike', 19, True]"""
    try:
        parts = shlex.split(values_str)
        result = []
        for val in parts:
            if val.lower() == "true":
                result.append(True)
            elif val.lower() == "false":
                result.append(False)
            else:
                try:
                    result.append(int(val))
                except ValueError:
                    result.append(val)
        return result
    except Exception:
        print(f"Некорректные значения: {values_str}")
        return None


def parse_set_clause(set_str):
    """Преобразует 'column = value' в словарь {column: value}"""
    return parse_where_clause(set_str)


def print_help():
    """Печать справки"""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> insert into <имя_таблицы> values (<значение1>, ...) - " +
      "добавить запись")
    print("<command> select from <имя_таблицы> [where <столбец>=<значение>] - " +
      "вывести записи")
    print("<command> update <имя_таблицы> set <столбец>=<значение> where <условие> -" +
      "обновить")
    print("<command> delete from <имя_таблицы> where <столбец>=<значение> -" +
      "удалить запись")
    print("<command> info <имя_таблицы> - информация о таблице")
    print("<command> exit - выйти")
    print("<command> help - справка\n")


# __________________________
# Ура! Ура! Ура! Игра! (игровой цикл)
# __________________________

def run():
    print("=== DB project is running! ===")
    metadata = load_metadata(METADATA_FILE)

    while True:
        try:
            user_input = input(">>> Введите команду: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы.")
            break

        if not user_input:
            continue

        args = shlex.split(user_input)
        cmd = args[0].lower()
        params = args[1:]


        # exit
        if cmd == "exit":
            print("Выход из программы.")
            break


        # help
        elif cmd == "help":
            print_help()


        # create_table
        elif cmd == "create_table":
            if len(params) < 2:
                print("Ошибка: недостаточно аргументов для create_table")
                continue
            table_name = params[0]
            columns_input = params[1:]
            if table_name in metadata:
                print(f'Ошибка: Таблица "{table_name}" уже существует.')
                continue

            columns = [("ID", "int")]
            valid_types = {"int", "str", "bool"}
            error = False
            for col in columns_input:
                if ":" not in col:
                    print(f"Некорректное значение: {col}. Используйте формат name:type")
                    error = True
                    break
                name, typ = col.split(":")
                if typ not in valid_types:
                    print(f"Некорректный тип: {typ}. Допустимы int, str, bool")
                    error = True
                    break
                columns.append((name, typ))
            if error:
                continue

            metadata[table_name] = columns
            save_metadata(METADATA_FILE, metadata)
            columns_str = ", ".join(f"{n}:{t}" for n, t in columns)
            print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')


        # drop_table
        elif cmd == "drop_table":
            if len(params) != 1:
                print("Ошибка: укажите имя таблицы для удаления")
                continue
            table_name = params[0]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            del metadata[table_name]
            save_metadata(METADATA_FILE, metadata)

            data_file = DATA_DIR / f"{table_name}.json"
            if data_file.exists():
                data_file.unlink()
            print(f'Таблица "{table_name}" успешно удалена.')


        # list_tables
        
        elif cmd == "list_tables":
            if metadata:
                for t in metadata:
                    print(f"- {t}")
            else:
                print("Нет таблиц.")

        # insert
        elif (cmd == "insert" and len(params) >= 3 and 
              params[0] == "into" and params[2] == "values"):
            table_name = params[1]
            table_data = load_table_data(table_name)
            values_str = user_input.split("values", 1)[1].strip()
            if values_str.startswith("(") and values_str.endswith(")"):
                values_str = values_str[1:-1].strip()
            values = parse_values(values_str)
            if values is None:
                continue
            table_data = insert(metadata, table_name, values, table_data)
            save_table_data(table_name, table_data)


        # Select
        elif cmd == "select" and len(params) >= 2 and params[0] == "from":
            table_name = params[1]
            table_data = load_table_data(table_name)
            if "where" in params:
                idx = params.index("where")
                where_clause = parse_where_clause(" ".join(params[idx + 1:]))
                if where_clause is None:
                    continue
            else:
                where_clause = None
            select(table_data, where_clause)

        # Update
        elif cmd == "update":
            table_name = params[0]
            if "set" not in params or "where" not in params:
                print("Ошибка: неверный синтаксис update")
                continue
            idx_set = params.index("set")
            idx_where = params.index("where")
            set_clause = parse_set_clause(" ".join(params[idx_set + 1:idx_where]))
            where_clause = parse_where_clause(" ".join(params[idx_where + 1:]))
            if set_clause is None or where_clause is None:
                continue
            table_data = load_table_data(table_name)
            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)

        # Delete
        elif (cmd == "delete" and len(params) >= 4 and 
              params[0] == "from" and "where" in params):
            table_name = params[1]
            idx_where = params.index("where")
            where_clause = parse_where_clause(" ".join(params[idx_where + 1:]))
            if where_clause is None:
                continue
            table_data = load_table_data(table_name)
            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)

        # Info
        elif cmd == "info" and len(params) == 1:
            table_name = params[0]
            table_data = load_table_data(table_name)
            info_table(metadata, table_data, table_name)


        # Неизвестная команда
        else:
            print(f'Функции "{cmd}" нет. Попробуйте снова.')