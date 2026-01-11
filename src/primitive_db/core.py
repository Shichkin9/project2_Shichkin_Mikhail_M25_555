from prettytable import PrettyTable

VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = [("ID", "int")]  
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        name, typ = col.split(":")
        if typ not in VALID_TYPES:
            print(f"Некорректное значение: {typ}. Попробуйте снова.")
            return metadata
        table_columns.append((name, typ))

    metadata[table_name] = table_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: ' +
          ", ".join(f"{name}:{typ}" for name, typ in table_columns))
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def insert(metadata, table_name, values, table_data):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name][1:] 
    if len(values) != len(columns):
        print(f"Некорректное количество значений. Ожидается {len(columns)}.")
        return table_data

    # Проверка
    record = {}
    for (col_name, col_type), val in zip(columns, values):
        if col_type == "int":
            if not isinstance(val, int):
                print(f"Некорректное значение: {val} для столбца {col_name}")
                return table_data
        elif col_type == "str":
            if not isinstance(val, str):
                print(f"Некорректное значение: {val} для столбца {col_name}")
                return table_data
        elif col_type == "bool":
            if not isinstance(val, bool):
                print(f"Некорректное значение: {val} для столбца {col_name}")
                return table_data
        record[col_name] = val

    # Генерация id

    if table_data:
        max_id = max(r["ID"] for r in table_data)
        record["ID"] = max_id + 1
    else:
        record["ID"] = 1

    table_data.append(record)
    print(f'Запись с ID={record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select(table_data, where_clause=None):
    """Вывод данных с фильтром (или всех)"""
    if where_clause:
        filtered = [
            r for r in table_data
            if all(r.get(k) == v for k, v in where_clause.items())
        ]
    else:
        filtered = table_data

    if not filtered:
        print("Записи не найдены.")
        return

    if filtered:
        table = PrettyTable()
        table.field_names = filtered[0].keys()
        for row in filtered:
            table.add_row([row[k] for k in row.keys()])
        print(table)


def update(table_data, set_clause, where_clause):
    updated = 0
    for r in table_data:
        if all(r.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                r[k] = v
            updated += 1
    if updated == 0:
        print("Записи не найдены.")
    else:
        print(f"Записи ({updated}) успешно обновлены.")
    return table_data


def delete(table_data, where_clause):
    initial_len = len(table_data)
    table_data = [
    r for r in table_data 
    if not all(r.get(k) == v for k, v in where_clause.items())]
    deleted = initial_len - len(table_data)
    if deleted == 0:
        print("Записи не найдены.")
    else:
        print(f"Записи ({deleted}) успешно удалены.")
    return table_data


def info_table(metadata, table_data, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    columns = metadata[table_name]
    print(f"Таблица: {table_name}")
    print("Столбцы: " + ", ".join(f"{n}:{t}" for n, t in columns))
    print(f"Количество записей: {len(table_data)}")

def list_tables(metadata):
    if not metadata:
        print("Таблицы отсутствуют.")
        return
    for table in metadata.keys():
        print(f"- {table}")