VALID_TYPES = ("int", "str", "bool")


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = ["ID:int"]
    for column in columns:
        name, _, column_type = column.partition(":")
        if not name or column_type not in VALID_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        table_columns.append(column)

    metadata[table_name] = table_columns
    columns_text = ", ".join(table_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_text}')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def is_valid_type(value, column_type):
    if column_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if column_type == "str":
        return isinstance(value, str)
    return isinstance(value, bool)


def matches(record, where_clause):
    for column, value in where_clause.items():
        if record.get(column) != value:
            return False
    return True


def insert(metadata, table_name, values, table_data):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name][1:]
    if len(values) != len(columns):
        print(
            f"Некорректное значение: ожидается {len(columns)} значений, "
            f"получено {len(values)}. Попробуйте снова."
        )
        return table_data

    record = {}
    for column, value in zip(columns, values):
        name, column_type = column.split(":")
        if not is_valid_type(value, column_type):
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return table_data
        record[name] = value

    new_id = max((row["ID"] for row in table_data), default=0) + 1
    table_data.append({"ID": new_id, **record})
    return table_data


def select(table_data, where_clause=None):
    if not where_clause:
        return table_data
    return [row for row in table_data if matches(row, where_clause)]


def update(table_data, set_clause, where_clause):
    for row in table_data:
        if matches(row, where_clause):
            row.update(set_clause)
    return table_data


def delete(table_data, where_clause):
    return [row for row in table_data if not matches(row, where_clause)]